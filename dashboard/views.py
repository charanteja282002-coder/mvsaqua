import urllib.parse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.text import slugify
from django.db.models import Sum
from store.models import Category, Product, Review
from orders.models import Order, OrderItem

def dash_login(request):
    if request.user.is_authenticated and request.user.is_staff: return redirect('dash_home')
    if request.method=='POST':
        u=authenticate(request,username=request.POST.get('username'),password=request.POST.get('password'))
        if u and u.is_staff: login(request,u); return redirect('dash_home')
        messages.error(request,'Invalid credentials.')
    return render(request,'dashboard/login.html')

def dash_logout(request): logout(request); return redirect('dash_login')

@login_required
def dash_home(request):
    orders=Order.objects.all()
    revenue=orders.aggregate(t=Sum('total'))['t'] or 0
    return render(request,'dashboard/home.html',{
        'total_orders':orders.count(),'pending':orders.filter(status='pending').count(),
        'dispatched':orders.filter(status='dispatched').count(),
        'delivered':orders.filter(status='delivered').count(),
        'total_products':Product.objects.filter(is_active=True).count(),
        'revenue':revenue,'recent_orders':orders[:12],
        'low_stock':Product.objects.filter(stock__lt=5,is_active=True)[:5],
    })

@login_required
def dash_products(request):
    qs=Product.objects.select_related('category').all()
    q=request.GET.get('q','')
    if q: qs=qs.filter(name__icontains=q)
    return render(request,'dashboard/products.html',{'products':qs,'q':q,'total':qs.count()})

@login_required
def product_form(request, pk=None):
    product=get_object_or_404(Product,pk=pk) if pk else None
    categories=Category.objects.all()
    if request.method=='POST':
        name=request.POST.get('name','').strip()
        if not name: messages.error(request,'Name required.'); return render(request,'dashboard/product_form.html',{'product':product,'categories':categories})
        slug=slugify(name)
        if Product.objects.filter(slug=slug).exclude(pk=pk).exists(): slug=f'{slug}-{Product.objects.count()}'
        data=dict(name=name,slug=slug,category_id=request.POST.get('category'),
            description=request.POST.get('description',''),care_tips=request.POST.get('care_tips',''),
            price=request.POST.get('price',0),offer_price=request.POST.get('offer_price') or None,
            weight_kg=request.POST.get('weight_kg',0.2),stock=request.POST.get('stock',50),
            is_featured='is_featured' in request.POST,is_new_arrival='is_new_arrival' in request.POST,
            is_bestseller='is_bestseller' in request.POST,is_active='is_active' in request.POST)
        if product:
            for k,v in data.items(): setattr(product,k,v)
            if request.FILES.get('image'): product.image=request.FILES['image']
            if request.FILES.get('image2'): product.image2=request.FILES['image2']
            product.save(); messages.success(request,f'"{product.name}" updated!')
        else:
            product=Product(**data)
            if request.FILES.get('image'): product.image=request.FILES['image']
            product.save(); messages.success(request,f'"{product.name}" created!')
        return redirect('dash_products')
    return render(request,'dashboard/product_form.html',{'product':product,'categories':categories})

@login_required
def product_delete(request, pk):
    p=get_object_or_404(Product,pk=pk); name=p.name; p.delete()
    messages.success(request,f'"{name}" deleted.'); return redirect('dash_products')

@login_required
def dash_orders(request):
    qs=Order.objects.all(); sf=request.GET.get('status','')
    if sf: qs=qs.filter(status=sf)
    counts={s:Order.objects.filter(status=s).count() for s,_ in Order.STATUS}
    return render(request,'dashboard/orders.html',{'orders':qs,'sf':sf,'counts':counts,'STATUS':Order.STATUS})

@login_required
def dash_order(request, pk):
    order=get_object_or_404(Order,pk=pk)
    if request.method=='POST':
        order.status=request.POST.get('status',order.status)
        order.courier=request.POST.get('courier',order.courier)
        order.tracking_no=request.POST.get('tracking_no',order.tracking_no)
        dd=request.POST.get('dispatch_date')
        if dd: order.dispatch_date=dd
        order.notes=request.POST.get('notes',order.notes)
        order.save(); messages.success(request,f'Order {order.order_id} updated!')
        return redirect('dash_order',pk=pk)
    def wa(num,msg): return f"https://wa.me/91{num}?text={urllib.parse.quote(msg)}"
    cn=dict(Order.COURIER).get(order.courier,'courier')
    confirm_msg=(f"✅ *Order Confirmed – MVS AQUA*\n\nHi {order.full_name} 👋🏻\n\n"
        f"Your order *{order.order_id}* is confirmed! 🎉\nTotal: ₹{order.total}\n\n"
        f"📅 We dispatch every *Monday*.\nTracking ID will be sent once dispatched.\n\nThank you 🥰 — MVS AQUA")
    dispatch_msg=(f"🚚 *Dispatched – MVS AQUA*\n\nHi {order.full_name} 👋🏻\n\n"
        f"Order *{order.order_id}* dispatched!\n\n📦 Courier: *{cn}*\n🆔 Tracking: *{order.tracking_no or 'N/A'}*\n"
        f"🔗 Track: {order.tracking_url or 'https://www.tpcindia.com/'}\n\n"
        f"⚠️ Track & collect tomorrow. Record *unboxing video* on opening.\n\nThank you! — MVS AQUA")
    return render(request,'dashboard/order_detail.html',{
        'order':order,'wa_confirm':wa(order.mobile,confirm_msg),'wa_dispatch':wa(order.mobile,dispatch_msg),
        'STATUS':Order.STATUS,'COURIER':Order.COURIER})

@login_required
def dash_categories(request):
    cats=Category.objects.all()
    if request.method=='POST':
        name=request.POST.get('name','').strip()
        if name:
            Category.objects.get_or_create(slug=slugify(name),
                defaults={'name':name,'emoji':request.POST.get('emoji','🐠'),'sort_order':request.POST.get('sort_order',0)})
            messages.success(request,f'Category "{name}" added!')
        return redirect('dash_categories')
    return render(request,'dashboard/categories.html',{'categories':cats})

@login_required
def dash_reviews(request):
    rvs=Review.objects.all()
    if request.method=='POST':
        action=request.POST.get('action')
        if action=='add':
            Review.objects.create(name=request.POST['name'],location=request.POST.get('location',''),
                rating=request.POST.get('rating',5),title=request.POST.get('title',''),body=request.POST['body'])
            messages.success(request,'Review added!')
        elif action=='delete': Review.objects.filter(pk=request.POST.get('pk')).delete()
        return redirect('dash_reviews')
    return render(request,'dashboard/reviews.html',{'reviews':rvs})
