from django.shortcuts import render, get_object_or_404
from .models import products
from category.models import category

# Create your views here.
def store(request, category_slug=None):
    categories = None
    product = None

    if category_slug != None:   
        categories = get_object_or_404(category, slug=category_slug)
        product = products.objects.filter(category=categories, is_available=True)
        product_count = product.count()
    else:
        product = products.objects.all().filter(is_available=True)
        product_count = product.count()
    context = {
        'products': product,
        'product_count': product_count
    }

    return render(request, 'store/store.html', context )

def product_detail(request, category_slug, product_slug):
    try:
        single_product = products.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    context = {
        'single_product': single_product
    }
    return render(request, 'store/product_detail.html', context)