from pages.models import Package


class Cart:
    """
    initialize the cart
    """

    def __int__(self, request):
        self.request = request
        self.session = request.session

        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart

    def add(self, product, quantity=1):

        """
        add product to cart
        """
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': quantity}
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        """
        save the new values in session
        """
        self.session.modified = True

    def remove(self, product):
        """
         remove product from cart
        """
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()

        products = Package.objects.filter(id__in=product_ids)

        cart = self.cart.copy()  # I don't want to change the cart, so I copy it because when i copy
        # a things, the main don't change, here self.cart will never change, and cart will change

        for product in products:
            cart[str(product.id)]['product_obj'] = product

        for item in cart.values():
            yield item

    def __len__(self):
        return len(self.cart.keys())

    def clear(self):
        del self.session['cart']
        self.save()

    def total_price(self):
        product_ids = self.cart.keys()
        products = Package.objects.filter(id__in=product_ids)

        return sum(product.price for product in products)











