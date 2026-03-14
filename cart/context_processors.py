def cart_context(request):
    cart = request.session.get('cart', {})
    count = sum(v.get('qty',0) for v in cart.values())
    total = sum(float(v.get('price',0))*v.get('qty',0) for v in cart.values())
    return {'cart_count': count, 'cart_total': round(total,2)}
