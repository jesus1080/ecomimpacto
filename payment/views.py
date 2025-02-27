from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAdrress, Order, OrderItem
from django.contrib import messages
from store.models import Product
import datetime
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
        #crear session con la informacion de envio
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping
        # Verificar si el usuario esta autenticado
        if request.user.is_authenticated:
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {'products': cart_products, 'quantities': quantities, 'totals': totals, 'shipping_info': request.POST, 'billing_form': billing_form} )
        else:
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {'products': cart_products, 'quantities': quantities, 'totals': totals, 'shipping_info': request.POST, 'billing_form': billing_form} )
        
        
    
    else:
        messages.success(request, ("Acceso Denegado"))
        return redirect('home')
    

def process_order(request):
    if request.POST: 
        cart = Cart(request)
        cart_products = cart.get_prods
        #cantidad de productos por unidad en el cart
        quantities = cart.get_quants
        totals = cart.cart_total()  
        #obtenemos la informacion de factura para la ultima page
        payment_form = PaymentForm(request.POST or None)
        # obtener data de envio de la session
        my_shipping = request.session.get('my_shipping')
        # Gather=recopilar informacion de orden
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        #crear direccion de envio para la informacion de sesion
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n"
        amount_paid = totals

        #crear una orden
        if request.user.is_authenticated:
            user = request.user

            create_order = Order(user=user, full_name=full_name, email=email, shipping_address = shipping_address, amount_paid=amount_paid)
            create_order.save()

            #adicionar items a la orden
            order_id = create_order.pk

            for product in cart_products():
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                #get cantidad
                for key, value in quantities().items():
                    if int(key) == product.id:
                        # create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                        create_order_item.save()
            
            #delete our car
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]

            messages.success(request, "Orden Enviada...")
            return redirect('home')
        else:
            #no logeado
            create_order = Order(full_name=full_name, email=email, shipping_address = shipping_address, amount_paid=amount_paid)
            create_order.save()

            #adicionar items a la orden
            order_id = create_order.pk

            for product in cart_products():
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                #get cantidad
                for key, value in quantities().items():
                    if int(key) == product.id:
                        # create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
                        create_order_item.save()

            #delete our car
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]

            messages.success(request, "Orden Enviada...")
            return redirect('home')

      

    else:
        messages.success(request, "Acceso denegado")
        return redirect('home')
    
def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            now = datetime.datetime.now()
            order = Order.objects.filter(id=num)
            order.update(shipped=False)
       
            messages.success(request, "Estado del pedido actualizado")
        return render(request, "payment/shipped_dash.html", {"orders": orders} )
    else:
        messages.success(request, "Acceso Denegado")
        return redirect('home')

def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            order = Order.objects.filter(id=num)
            now = datetime.datetime.now()
            order.update(shipped=True, date_shipped = now)
       
            messages.success(request, "Estado del pedido actualizado")




        return render(request, "payment/not_shipped_dash.html", {"orders": orders} )
    else:
        messages.success(request, "Acceso Denegado")
        return redirect('home')
    
def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser: 

        order = Order.objects.get(id=pk)

        items = OrderItem.objects.filter(order=pk)

        if request.POST:
            status = request.POST['shipping_status']

            if status == "true":
                order = Order.objects.filter(id=pk)
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped = now)
            else:
                order = Order.objects.filter(id=pk)
                order.update(shipped=False)
            messages.success(request, "Estado del pedido actualizado")

        return render(request, 'payment/orders.html', {"order":order, "items":items})
    else:
        messages.success(request, "Acceso Denegado")
        return redirect('home')