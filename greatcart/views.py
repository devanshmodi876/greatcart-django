from django.shortcuts import render
from store.models import products

def home(request):
    product = products.objects.all().filter(is_available=True)

    context = {
        'products': product,
    }
    
    return render(request, 'home.html', context)