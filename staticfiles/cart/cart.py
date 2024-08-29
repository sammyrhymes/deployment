
class Cart():
    def __init__(self, request):
        
        self.session = request.session

        #get the current session key if it exists 
        cart = self.session.get('session_key')

        #if user is new, no session key! create one.
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # make sure cart is available in all pages of the sight
        self.cart = cart
