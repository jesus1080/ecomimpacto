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