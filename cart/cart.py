"""
This file contains the shopping cart logic.
The cart is stored in the user's session (not in the database), which means
it's kept even if the user hasn't logged in yet.
"""
from products.models import Product

CART_SESSION_KEY = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if cart is None:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        """
        Add a product to the cart, or increase its quantity if it's already there.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0}
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def update(self, product_id, quantity):
        """
        Set a product's quantity in the cart directly to a specific value.
        """
        product_id = str(product_id)
        if product_id in self.cart and quantity > 0:
            self.cart[product_id]['quantity'] = quantity
            self.save()

    def remove(self, product_id):
        """
        Remove a product from the cart.
        """
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        """
        Mark the session as modified so Django saves it.
        """
        self.session.modified = True

    def clear(self):
        """
        Empty the cart completely (used after a successful checkout).
        """
        self.session[CART_SESSION_KEY] = {}
        self.save()

    def __iter__(self):
        """
        Iterate over the cart items, linking them to the real Product objects
        from the database.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        products_map = {str(p.id): p for p in products}

        for product_id, item in self.cart.items():
            product = products_map.get(product_id)
            if product is None:
                continue
            yield {
                'product': product,
                'quantity': item['quantity'],
                'total_price': product.price * item['quantity'],
            }

    def __len__(self):
        """
        Total number of items in the cart (sum of all quantities).
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Calculate the overall total price of everything in the cart.
        """
        total = 0
        for item in self:
            total += item['total_price']
        return total
