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

        messages.success(self.request, _("a product added to cart"))

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
        if self.cart:
            product_ids = self.cart.keys()
           # cart = self.cart.copy()  # I don't want to change the cart, so I copy it because when I copy
                    # a things, the main don't change, here self.cart will never change, and cart will change

            for id in product_ids:
                product = Package.objects.filter(id=id)
                if product is True:
                    product_id = str(product.id)
                    self.cart[product_id]['product_obj'] += product
                    self.cart[product_id] = {'quantity': self.cart.product_id.quantity}

                    if self.cart.values().__len__() > 0:
                        for item in self.cart.values():
                                item['total_price'] = item['product_obj'].price * item['quantity']
                                yield item
                # else:
                #     self.clear()

    def __len__(self):
        # return len(self.cart.keys()) its show only product length without quantity
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session['cart']
        messages.success(self.request, _("cart get empty"))
        self.save()

    def total_price(self):
        product_ids = self.cart.keys()

        for item in self.cart.values():
            if item and self.cart.values().__len__() > 1 :
                total = sum(item['quantity'] * item['product_obj'].price)
            else:total=''
            return total
        # return sum(item['quantity'] * item['product_obj'].price for item in self.cart.values())
