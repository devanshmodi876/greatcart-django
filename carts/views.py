from django.shortcuts import render
from store.models import products
from .models import Cart, CartItem
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse

# Create your views here.

def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id

def add_cart(request, product_id):
    color = request.GET['color']
    size = request.GET['size']

    product = products.objects.get(id=product_id)
    cart_id = _cart_id(request)
    try:
        cart = Cart.objects.get(cart_id=cart_id)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = cart_id
        )
    cart.save()

    try:
        cartItem = CartItem.objects.get(product=product, cart=cart)
        cartItem.quantity += 1
        cartItem.save()
    except CartItem.DoesNotExist:
        cartItem = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cartItem.save()                 
    return redirect('cart') 

def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(products , id=product_id)
    cartItem = CartItem.objects.get(product=product, cart=cart)
    if cartItem.quantity > 1:
        cartItem.quantity -= 1
        cartItem.save()
    else:
        cartItem.delete()
    return redirect('cart')

def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(products , id=product_id)
    cartItem = CartItem.objects.get(product=product, cart=cart)
    cartItem.delete()
    return redirect('cart')

def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html',context)