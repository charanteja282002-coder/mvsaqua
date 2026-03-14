import io, urllib.parse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from .models import Order, OrderItem
from store.models import Product
from cart.views import _cart, _save

def checkout(request):
    cart=_cart(request)
    if not cart: messages.warning(request,'Cart is empty!'); return redirect('cart_view')
    items=[]; subtotal=0.0; total_weight=0.0
    for pid,d in cart.items():
        try:
            p=Product.objects.get(pk=int(pid)); qty=d.get('qty',1)
            price=float(d.get('price',0)); wt=float(p.weight_kg)*qty; line=price*qty
            subtotal+=line; total_weight+=wt
            items.append({'product':p,'qty':qty,'price':price,'line_total':line,'line_weight':wt})
        except Product.DoesNotExist: pass
    shipping=round(total_weight*80,2); total=round(subtotal+shipping,2)

    if request.method=='POST':
        fn=request.POST.get('full_name','').strip(); mob=request.POST.get('mobile','').strip()
        addr=request.POST.get('address','').strip(); city=request.POST.get('city','').strip()
        state=request.POST.get('state','').strip(); pin=request.POST.get('pincode','').strip()
        if not all([fn,mob,addr,city,state,pin]):
            messages.error(request,'Please fill all required fields.'); 
            return render(request,'orders/checkout.html',{'items':items,'subtotal':subtotal,'shipping':shipping,'total':total})
        order=Order.objects.create(full_name=fn,mobile=mob,email=request.POST.get('email','').strip(),
            address=addr,landmark=request.POST.get('landmark','').strip(),
            city=city,state=state,pincode=pin,subtotal=subtotal,shipping=shipping,total=total)
        for pid,d in cart.items():
            try:
                p=Product.objects.get(pk=int(pid))
                OrderItem.objects.create(order=order,product=p,product_name=p.name,
                    price=d.get('price',0),qty=d.get('qty',1),weight_kg=p.weight_kg)
            except Product.DoesNotExist: pass
        _save(request,{})
        lines='\n'.join(f"  • {i['product'].name} ×{i['qty']} = ₹{i['line_total']:.0f}" for i in items)
        msg=(f"🛒 *NEW ORDER – MVS AQUA*\n\n🆔 *{order.order_id}*\n👤 {order.full_name}\n"
             f"📱 {order.mobile}\n📍 {order.address}{', '+order.landmark if order.landmark else ''}\n"
             f"    {order.city}, {order.state} – {order.pincode}\n\n📦 Items:\n{lines}\n\n"
             f"💰 Subtotal: ₹{subtotal:.0f}\n🚚 Shipping: ₹{shipping:.0f}\n💵 *TOTAL: ₹{total:.0f}*\n\n"
             f"Please confirm & share payment details 🙏🏻")
        wa=f"https://wa.me/{settings.ADMIN_WHATSAPP}?text={urllib.parse.quote(msg)}"
        return render(request,'orders/success.html',{'order':order,'wa':wa,'items':items})
    return render(request,'orders/checkout.html',{'items':items,'subtotal':subtotal,'shipping':shipping,'total':total})

def track(request):
    order=None; error=None
    oid=(request.POST.get('order_id') or request.GET.get('q','')).strip().upper()
    if oid:
        try: order=Order.objects.prefetch_related('items').get(order_id=oid)
        except Order.DoesNotExist: error=f'No order found for "{oid}". Please check and try again.'
    status_steps=[('pending','Pending'),('confirmed','Confirmed'),('processing','Processing'),
                  ('dispatched','Dispatched'),('delivered','Delivered')]
    done_map={'pending':0,'confirmed':1,'processing':2,'dispatched':3,'delivered':4,'cancelled':-1}
    order_done_idx=done_map.get(order.status if order else '',0)
    return render(request,'orders/track.html',{
        'order':order,'error':error,'oid':oid,
        'status_steps':status_steps,'order_done_idx':order_done_idx
    })

def invoice_pdf(request, order_id):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm

    order=get_object_or_404(Order,order_id=order_id)
    buf=io.BytesIO()
    doc=SimpleDocTemplate(buf,pagesize=A4,topMargin=12*mm,bottomMargin=12*mm,leftMargin=15*mm,rightMargin=15*mm)
    styles=getSampleStyleSheet(); aqua=colors.HexColor('#0077B6'); dark=colors.HexColor('#023E8A')
    story=[]
    H1=ParagraphStyle('H1',fontSize=22,fontName='Helvetica-Bold',textColor=aqua,spaceAfter=2)
    SM=ParagraphStyle('SM',fontSize=9,textColor=colors.grey,spaceAfter=6)
    story.append(Paragraph('MVS AQUA',H1))
    story.append(Paragraph('WhatsApp: +91 9490255775 | Instagram: @Mvs_aqua | Prepaid Orders Only',SM))
    story.append(HRFlowable(width='100%',thickness=2,color=aqua,spaceAfter=8))
    hd=[[Paragraph(f'<b>INVOICE #{order.order_id}</b>',ParagraphStyle('B',fontSize=13,fontName='Helvetica-Bold')),
         Paragraph(f'<b>Date:</b> {order.created_at.strftime("%d %b %Y")}<br/><b>Status:</b> {order.get_status_display()}',
                   ParagraphStyle('R',fontSize=10,alignment=2))]]
    ht=Table(hd,colWidths=[95*mm,85*mm]); ht.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP')])); story.append(ht)
    story.append(Spacer(1,5*mm))
    cd=[[Paragraph('<b>CUSTOMER</b>',ParagraphStyle('h',fontName='Helvetica-Bold',fontSize=9,textColor=dark)),
         Paragraph('<b>DELIVERY ADDRESS</b>',ParagraphStyle('h2',fontName='Helvetica-Bold',fontSize=9,textColor=dark))],
        [Paragraph(f'{order.full_name}<br/>📱 {order.mobile}',styles['Normal']),
         Paragraph(f'{order.address}{"<br/>"+order.landmark if order.landmark else ""}<br/>{order.city}, {order.state} – {order.pincode}',styles['Normal'])]]
    ct=Table(cd,colWidths=[95*mm,85*mm])
    ct.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E0F7FA')),
        ('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#B2EBF2')),('PADDING',(0,0),(-1,-1),8)]))
    story.append(ct); story.append(Spacer(1,6*mm))
    rows=[['#','Product','Qty','Unit Price','Weight','Amount']]
    for i,itm in enumerate(order.items.all(),1):
        rows.append([str(i),itm.product_name,str(itm.qty),f'Rs.{float(itm.price):.2f}',f'{float(itm.weight_kg):.3f}kg',f'Rs.{itm.line_total:.2f}'])
    rows+=[['','','','','Subtotal',f'Rs.{float(order.subtotal):.2f}'],
           ['','','','','Shipping (Rs.80/kg)',f'Rs.{float(order.shipping):.2f}'],
           ['','','','','TOTAL',f'Rs.{float(order.total):.2f}']]
    pt=Table(rows,colWidths=[10*mm,78*mm,14*mm,27*mm,26*mm,25*mm])
    pt.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),aqua),('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#B2EBF2')),
        ('PADDING',(0,0),(-1,-1),7),('ROWBACKGROUNDS',(0,1),(-1,-4),[colors.white,colors.HexColor('#F0FBFF')]),
        ('BACKGROUND',(0,-3),(-1,-1),colors.HexColor('#E0F7FA')),
        ('FONTNAME',(4,-1),(5,-1),'Helvetica-Bold'),('FONTSIZE',(4,-1),(5,-1),12),
        ('LINEABOVE',(0,-3),(-1,-3),1.5,dark),('ALIGN',(2,0),(-1,-1),'CENTER')]))
    story.append(pt); story.append(Spacer(1,8*mm))
    story.append(Paragraph('<b>Thank you for choosing MVS AQUA! 🐠</b>',ParagraphStyle('ty',fontSize=12,textColor=aqua,fontName='Helvetica-Bold',spaceAfter=4)))
    story.append(Paragraph('⚠️ No replacement without unboxing video. Report damage within 24hrs. Only prepaid. No COD.',ParagraphStyle('note',fontSize=8,textColor=colors.grey)))
    doc.build(story); buf.seek(0)
    resp=HttpResponse(buf,content_type='application/pdf')
    resp['Content-Disposition']=f'attachment; filename="MVS_AQUA_{order.order_id}.pdf"'
    return resp
