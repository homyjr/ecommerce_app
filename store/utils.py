class dotdict(dict):
    
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class Cart:
     
    """ cart management without user loggedin"""

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('skey')
    
        if 'skey' not in request.session:
            cart = self.session['skey'] = {}
        print(cart)
        self.cart = cart


    def add_to_cart(self, product):
        product_id = product.id    

        if product_id not in self.cart:
           self.cart[str(product_id)] = {'price': str(product.price), 'quantity':'1'}

        self.session.modified = True
    
    @property
    def total_price(self):     
        
        return sum((int(item['quantity']))*(float(item['price'])) for item in self.cart.values())    

    def price(self, product_id):
        item = self.cart[str(product_id)]
        return (int(item['quantity']))*(float(item['price']))

    @property
    def get_items(self) -> str:
        return self.cart


    def updatecart(self, product_id, action):
        price = 0
        total_price = 0
        quantity = 0
        

        item = self.cart[str(product_id)]
        if action == 'add':
           item['quantity'] = str(int(item['quantity']) +1)
        elif action == 'subtract':
            item['quantity'] = str(int(item['quantity']) -1)
        else:
            self.cart.pop(str(product_id))

        if str(product_id) in self.cart.keys():
           if int(item['quantity']) <1:
               self.cart.pop(str(product_id))

        self.session.modified = True       
               
        if str(product_id) in self.cart.keys():       
           price = self.price(product_id)
           total_price = self.total_price
           quantity = int(self.cart[str(product_id)]['quantity'])
            
        
               
        

        return price, total_price, quantity


        

    
                                                       

