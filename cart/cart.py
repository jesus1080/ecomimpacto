from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session

        self.request = request

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

        #tratar con el usuario conectado
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # convertir {'3':1, '2':4} to {"3":1, "2":4} cantidad y producto
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # guardar los items del carrito
            current_user.update(old_cart=str(carty))




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

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # convertir {'3':1, '2':4} to {"3":1, "2":4} cantidad y producto
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # guardar los items del carrito
            current_user.update(old_cart=str(carty))
        thing = self.cart
        return thing
    
    def delete(self,product):
        product_id = str(product)

        if product_id in self.cart:
           del self.cart[product_id] 

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # convertir {'3':1, '2':4} to {"3":1, "2":4} cantidad y producto
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # guardar los items del carrito
            current_user.update(old_cart=str(carty))

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
    
    def db_add(self,product,quantity):
        product_id = str(product)
        product_qty = str(quantity)
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)


        self.session.modified = True

        #tratar con el usuario conectado
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # convertir {'3':1, '2':4} to {"3":1, "2":4} cantidad y producto
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # guardar los items del carrito
            current_user.update(old_cart=str(carty))