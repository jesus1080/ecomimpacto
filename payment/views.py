from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAdrress
from django.contrib import messages
# Create your views here.
def payment_success(request):
    return render(request, "payment/payment_success.html", {})

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    #cantidad de productos por unidad en el cart
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        #ingreso como registrado
        shipping_user = ShippingAdrress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, "payment/checkout.html", {'products': cart_products, 'quantities': quantities, 'totals': totals, 'shipping_form': shipping_form} )
    else:
        #ingreso como invitado
        shipping_form = ShippingForm(request.POST or None)
        return render(request, "payment/checkout.html", {'products': cart_products, 'quantities': quantities, 'totals': totals, 'shipping_form': shipping_form} )

def billing_info(request):
    if request.POST:
    
        cart = Cart(request)
        cart_products = cart.get_prods
        #cantidad de productos por unidad en el cart
        quantities = cart.get_quants
        totals = cart.cart_total()   
        # Verificar si el usuario esta autenticado

        if request.user.is_authenticated:
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {'products': cart_products, 'quantities': quantities, 'totals': totals, 'shipping_info': request.POST, 'billing_form': billing_form} )
        else:
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {'products': cart_products, 'quantities': quantities, 'totals': totals, 'shipping_info': request.POST, 'billing_form': billing_form} )
        shipping_form = request.POST
        return render(request, "payment/billing_info.html", {'products': cart_products, 'quantities': quantities, 'totals': totals, 'shipping_form': shipping_form} )
    
    else:
        messages.success(request, ("Acceso Denegado"))
        return redirect('home')