from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from store.models import Product

def _cart(req): return req.session.get('cart',{})
def _save(req,cart): req.session['cart']=cart; req.session.modified=True

def cart_view(request):
    cart=_cart(request); items=[]; subtotal=0.0; total_weight=0.0
    for pid,d in list(cart.items()):
        try:
            p=Product.objects.get(pk=int(pid))
            qty=d.get('qty',1); price=float(d.get('price',0))
            wt=float(p.weight_kg)*qty; line=price*qty
            subtotal+=line; total_weight+=wt
            items.append({'product':p,'qty':qty,'price':price,'line_total':line,'line_weight':wt})
        except Product.DoesNotExist:
            del cart[pid]; _save(request,cart)
    shipping=round(total_weight*80,2)
    return render(request,'cart/cart.html',{
        'items':items,'subtotal':round(subtotal,2),
        'shipping':shipping,'total':round(subtotal+shipping,2),
        'total_weight':round(total_weight,3)
    })

def cart_add(request, pk):
    p=get_object_or_404(Product,pk=pk)
    qty=max(1,min(int(request.POST.get('qty',1)),50))
    cart=_cart(request); pid=str(pk)
    if pid in cart: cart[pid]['qty']=min(cart[pid]['qty']+qty,50)
    else: cart[pid]={'name':p.name,'price':str(p.final_price),'qty':qty,'image':p.image.url if p.image else ''}
    _save(request,cart)
    if request.headers.get('X-Requested-With')=='XMLHttpRequest':
        return JsonResponse({'ok':True,'cart_count':sum(v['qty'] for v in cart.values()),'name':p.name})
    messages.success(request, f'"{p.name}" added to cart!')
    return redirect(request.POST.get('next','cart_view'))

def cart_update(request, pk):
    cart=_cart(request); pid=str(pk)
    qty=int(request.POST.get('qty',0))
    if pid in cart:
        if qty>0: cart[pid]['qty']=min(qty,50)
        else: del cart[pid]
        _save(request,cart)
    return redirect('cart_view')

def cart_remove(request, pk):
    cart=_cart(request); pid=str(pk)
    if pid in cart:
        messages.info(request,f'"{cart[pid].get("name","Item")}" removed.')
        del cart[pid]; _save(request,cart)
    return redirect('cart_view')
