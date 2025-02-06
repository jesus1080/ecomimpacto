from store.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session

        # obtener la llave de session actual si existe
        cart = self.session.get('session_key')

        # si el usuario es nuevo, no hay llave de session, crar una 
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        
        # estar seguro que cart es valido en todas las paginas del sitio
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = quantity
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)


        self.session.modified = True

    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        product_ids = self.cart.keys()
        # Buscar productos de la lista de card en la DB
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_quants(self):
        quentities = self.cart
        return quentities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        outcart = self.cart
        outcart[product_id] = product_qty

        self.session.modified = True

        thing = self.cart
        return thing
    
    def delete(self,product):
        product_id = str(product)

        if product_id in self.cart:
           del self.cart[product_id] 

        self.session.modified = True

    def cart_total(self):
        products_ids = self.cart.keys()

        products = Product.objects.filter(id__in=products_ids)

        quantities = self.cart

        total = 0
        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    #verificar si el producto esta a la venta
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)
        return total