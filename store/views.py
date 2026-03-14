from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Category, Product, Review

def home(request):
    return render(request, 'store/home.html', {
        'categories':  Category.objects.all(),
        'featured':    Product.objects.filter(is_featured=True, is_active=True)[:8],
        'new_arrivals':Product.objects.filter(is_new_arrival=True, is_active=True)[:8],
        'bestsellers': Product.objects.filter(is_bestseller=True, is_active=True)[:8],
        'reviews':     Review.objects.filter(rating__gte=4)[:8],
    })

def product_list(request):
    qs   = Product.objects.filter(is_active=True).select_related('category')
    sort = request.GET.get('sort','newest')
    if   sort=='price_low':  qs = qs.order_by('price')
    elif sort=='price_high': qs = qs.order_by('-price')
    elif sort=='popular':    qs = qs.filter(is_bestseller=True)
    else:                    qs = qs.order_by('-created_at')
    return render(request,'store/product_list.html',{
        'products':qs,'categories':Category.objects.all(),'sort':sort,'total':qs.count()
    })

def category_page(request, slug):
    category = get_object_or_404(Category, slug=slug)
    qs = Product.objects.filter(category=category,is_active=True)
    sort = request.GET.get('sort','newest')
    if sort=='price_low':    qs = qs.order_by('price')
    elif sort=='price_high': qs = qs.order_by('-price')
    else:                    qs = qs.order_by('-created_at')
    return render(request,'store/product_list.html',{
        'products':qs,'category':category,'categories':Category.objects.all(),
        'sort':sort,'total':qs.count()
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related = Product.objects.filter(category=product.category,is_active=True).exclude(pk=product.pk)[:6]
    return render(request,'store/product_detail.html',{'product':product,'related':related})

def search(request):
    q = request.GET.get('q','').strip()
    results = []
    if q:
        results = Product.objects.filter(
            Q(name__icontains=q)|Q(description__icontains=q)|Q(category__name__icontains=q),
            is_active=True
        ).distinct()
    return render(request,'store/search.html',{
        'results':results,'q':q,'categories':Category.objects.all()
    })
