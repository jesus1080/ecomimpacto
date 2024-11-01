from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

def cart_sumary(request):
    return render(request, "cart_sumary.html", {})

def cart_add(request):
    # obtener el cart
    cart = Cart(request)
    # test post
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product)
        response = JsonResponse({'Product Name': product.name})
        return response



def cart_delete(request):
    pass

def cart_update(request):
    pass
