from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

def cart_sumary(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    #cantidad de productos por unidad en el cart
    quantities = cart.get_quants
    return render(request, "cart_sumary.html", {'products': cart_products, 'quantities': quantities} )

def cart_add(request):
    # obtener el cart
    cart = Cart(request)
    # test post
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        #cantidad de producto a add to cart
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity = product_qty)
        #obtener cantidad de cart
        cart_quantity = cart.__len__()
        
        #response = JsonResponse({'Product Name': product.name})
        response = JsonResponse({'qty': cart_quantity})
        return response



def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))

        cart.delete(product=product_id)

        response = JsonResponse({'product': product_id})
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty': product_qty})
        return response
