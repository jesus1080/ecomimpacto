from django.shortcuts import render

def cart_sumary(request):
    return render(request, "cart_sumary.html", {})

def cart_add(request):
    pass

def cart_delete(request):
    pass

def cart_update(request):
    pass
