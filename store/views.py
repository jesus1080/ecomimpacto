from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAdrress
from django import forms
from django.db.models import Q
import json
from cart.cart import Cart

def category(request, cate): 
    try:
        category = Category.objects.get(name=cate)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'productos':products, 'category':category})
    except:
        messages.success(request, ("La categoria no existe"))
        return redirect('home')
    

def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})


def home(request):
    productos = Product.objects.all()
    return render(request, 'home.html', {'productos':productos})


def about(request):
    return render(request, 'about.html', {})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #Traer los productos del carrito si los tiene
            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart
            #convertir el string en python dictionary
            if saved_cart:
                #usamos json para convertir
                convert_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key, value in convert_cart.items():
                     cart.db_add(product=key, quantity=value)

            messages.success(request, ("Estas authenticado correctamente"))
            return redirect('home')
        else:
            messages.success(request, ("Hay un error"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})


    

def logout_user(request):
    logout(request)
    messages.success(request, ("Saliste copn exito... Gracias!"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Estas registrado correctamente"))
            return redirect('home')
        else:
            messages.success(request, ("Hay un problema con el registro"))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})
    
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "Usuario actualizado ")
            return redirect('home')
        return render(request, "update_user.html",{'user_form':user_form})
    else:
        messages.success(request, "Debes ingresar ")
        return redirect('home')


    
def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {"categories":categories})

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Su contrasena fue actualizada, por favor ingrese de nuevo")
                login(request, current_user)
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html",{'form': form})

    else:
       messages.success(request, "Usuario actualizado ")
       return redirect('home') 

def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        shipping_user = ShippingAdrress.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, "Informacion de Usuario actualizada ")
            return redirect('home')
        return render(request, "update_info.html",{'form':form, 'shipping_form': shipping_form})
    else:
        messages.success(request, "Debes ingresar ")
        return redirect('home')
  
def search(request):
    # determine if they filled otu the form
    if request.method == "POST":
        searched =  request.POST['searched']
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))

        if not searched:
           messages.success(request, "No existe producto con ese nombre...") 
           return render(request, "search.html", {})
        else:

            return render(request, "search.html", {'searched': searched})
    else:
        return render(request, "search.html", {})