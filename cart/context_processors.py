from .cart import Cart

# crear contexto del proses para que el cart funcione en todas las paginas

def cart(request):
    return {'cart': Cart(request)}