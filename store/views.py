from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms


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
    
def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {"categories":categories})