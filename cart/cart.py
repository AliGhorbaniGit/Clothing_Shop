from django.utils.translation import gettext as _
from django.contrib import messages
from copy import deepcopy

from shop.models import Product


class Cart:
    def __init__(self, request):
        """    Initialize the cart  """

        self.request = request
        self.session = request.session

        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart

    def add(self, product, size, color, quantity=1, replace_current_quantity=False):
        """   Add product to the cart   """

        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': quantity, 'color': color, 'size': size}

        elif replace_current_quantity:
            self.cart[product_id]['quantity'] += quantity
            self.cart[product_id]['color'] = color
            self.cart[product_id]['size'] = size

        else:
            self.cart[product_id]['quantity'] = quantity
            self.cart[product_id]['color'] = color
            self.cart[product_id]['size'] = size

        messages.success(self.request, _('Product successfully added to your cart'))
        self.save()

    def remove(self, product):

        """   Remove a product from the cart   """

        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            messages.success(self.request, _('Product successfully removed from your cart'))
            self.save()

        else:
            messages.success(self.request, _('there is not such this Product to be remove from your cart'))

    def save(self):
        """   Mark session as modified to save changes   """
        self.session.modified = True

    def __iter__(self):
        """   Marking cart iterable   """

        # cart = deepcopy(self.cart)
        # product_ids = self.cart.keys()
        #
        # for id in product_ids:
        #     # is 'get' ok here ??
        #     product = Product.objects.get(id=id)
        #     if product:
        #         pass
        #     else:
        #         del cart[str(id)]
        #         self.save()
        #
        # products = Product.objects.filter(id__in=product_ids)
        #
        # for product in products:
        #     cart[str(product.id)]['product_obj'] = product
        #
        # for item in cart.values():
        #     if item['product_obj'].is_offer:
        #         off = (item['product_obj'].price - (
        #                 (item['product_obj'].price * item['product_obj'].offer_percent) / 100))
        #         qua = item['quantity']
        #         item['total_price'] = int(off) * qua
        #     else:
        #         item['total_price'] = item['product_obj'].price * item['quantity']
        #
        #     yield item

        cart = deepcopy(self.cart)
        product_ids = list(self.cart.keys())

        for id in product_ids:
            try:
                product = Product.objects.get(id=id)
                cart[str(id)]['product_obj'] = product
            except Product.DoesNotExist:
                del cart[str(id)]
                self.save()

        for item in cart.values():
            if 'product_obj' in item:
                if item['product_obj'].is_offer:
                    off = (item['product_obj'].price - (
                            (item['product_obj'].price * item['product_obj'].offer_percent) / 100))
                    qua = item['quantity']
                    item['total_price'] = int(off) * qua
                else:
                    item['total_price'] = item['product_obj'].price * item['quantity']
                yield item

    def __len__(self):
        cart = deepcopy(self.cart)
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        if len(products) == 0:
            return 0
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):

        cart = deepcopy(self.cart)
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            cart[str(product.id)]['product_obj'] = product
        if len(products) == 0:
            return 0

        for product in products:
            cart[str(product.id)]['product_obj'] = product

        product_total_price = 0
        for item in cart.values():
            if item['product_obj'].is_offer:
                product_total_price += (item['product_obj'].price - (
                        (item['product_obj'].price * item['product_obj'].offer_percent) / 100)) * item['quantity']

            else:
                product_total_price += (item['product_obj'].price * item['quantity'])

        return int(product_total_price)

    def clear(self):
        del self.session['cart']
        self.save()

    def is_empty(self):
        if self.cart:
            return False
        return True
