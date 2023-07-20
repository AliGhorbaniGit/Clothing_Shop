from django.contrib import messages
from django.utils.translation import gettext as _

from pages.models import Package


class Cart:

    def __init__(self, request):
        self.request = request
        self.session = request.session

        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart

    def add(self, product, quantity=1, replace_current_quantity=False):

        """
        add product to cart
        """
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': quantity}
        if replace_current_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        messages.success(self.request,_("a product added to cart"))

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
            messages.warning(self.request, _("a product remove from cart"))
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()

        products = Package.objects.filter(id__in=product_ids)

        cart = self.cart.copy()  # I don't want to change the cart, so I copy it because when I copy
        # a things, the main don't change, here self.cart will never change, and cart will change

        for product in products:
            cart[str(product.id)]['product_obj'] = product

        for item in cart.values():
            item['total_price'] = item['product_obj'].price * item['quantity']
            yield item

    def __len__(self):
        return len(self.cart.keys())

    def clear(self):
        del self.session['cart']
        messages.success(self.request,_("cart get empty"))
        self.save()

    def total_price(self):
        product_ids = self.cart.keys()

        return sum(item['quantity'] * item['product_obj'].price for item in self.cart.values())

