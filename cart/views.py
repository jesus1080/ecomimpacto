from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

def cart_sumary(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    return render(request, "cart_sumary.html", {'products': cart_products})

def cart_add(request):
    # obtener el cart
    cart = Cart(request)
    # test post
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product)
        #obtener cantidad de cart
        cart_quantity = cart.__len__()
        
        #response = JsonResponse({'Product Name': product.name})
        response = JsonResponse({'qty': cart_quantity})
        return response



def cart_delete(request):
    pass

def cart_update(request):
    pass
