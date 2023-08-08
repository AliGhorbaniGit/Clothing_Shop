# from django.contrib import messages
# from django.utils.translation import gettext as _
#
# from pages.models import Package
#
#
# class Cart:
#     def __init__(self, request):
#         """  INITIALIZED THE CART :  """
#
#         self.request = request
#         self.session = request.session
#         cart = self.session.get('cart')
#
#         if not cart:
#             cart = self.session['cart'] = {}
#         self.cart = cart
#
#     def add(self, product, quantity=1, replace_current_quantity=False):
#         """     add product to cart :   """
#
#         product_id = str(product.id)
#
#         if product_id not in self.cart:
#             self.cart[product_id] = {'quantity': quantity}
#         if replace_current_quantity:
#             self.cart[product_id]['quantity'] = quantity
#         else:
#             self.cart[product_id]['quantity'] += quantity
#
#         messages.success(self.request, _("a product added to cart"))
#         self.save()
#
#     def save(self):
#         """     save new CHANGE IN session      """
#         self.session.modified = True
#
#     def remove(self, product):
#         """     remove product from carT     """
#
#         product_id = str(product.id)
#
#         if product_id in self.cart:
#             del self.cart[product_id]
#             messages.warning(self.request, _("a product remove from cart"))
#             self.save()
#
#     def __iter__(self):
#         """     MAKE THE CART ITERABLE      """
#         cart = self.session.get('cart')
#         if cart:
#             product_ids = cart.keys()
#             """     cart = self.cart.copy()  # I don't want to change the cart, so I copy it because when I copy
#              a things, the main don't change, here self.cart will never change, and cart will change    """
#
#             for id in product_ids:
#                 product = Package.objects.get(id=id)
#                 if product:
#                     product_id = str(product.id)
#                     self.cart[product_id]['product_obj'] = product
#                     self.cart[product_id] = {'quantity': cart.product_id.quantity}
#
#                     if cart.__len__() > 0:
#                         for item in self.cart.values():
#                             item['total_price'] = item['product_obj'].price * item['quantity']
#                             yield item
#                 # else:
#                 #     self.clear()
#
#     def __len__(self):
#         """    GET LENGTH OF CART  """
#
#         # return len(self.cart.keys()) its show only product length without quantity
#         return sum(item['quantity'] for item in self.cart.values())
#
#     def clear(self):
#         """    CLEAR CART  """
#         if self.session['cart']:
#             del self.session['cart']
#             messages.success(self.request, _("cart get empty"))
#         else:
#             messages.error(self.request, _("cart is empty already"))
#         self.save()
#
#     def total_price(self):
#         """     CALCULATE TOTAL PRICE OF CART ITEM'S """
#
#         product_ids = self.cart.keys()
#
#         for item in self.cart.values():
#             if item and self.cart.values().__len__() > 1:
#                 total = sum(item['quantity'] * item['product_obj'].price)
#             else:
#                 total = ''
#             return total
#         # return sum(item['quantity'] * item['product_obj'].price for item in self.cart.values())


# from django.utils.translation import gettext as _
# from django.contrib import messages
#
# from pages.models import Package
#
#
# class Cart:
#     def __init__(self, request):
#         """
#         Initialize the cart
#         """
#         self.request = request
#
#         self.session = request.session
#
#         cart = self.session.get('cart')
#
#         if not cart:
#             cart = self.session['cart'] = {}
#
#         self.cart = cart
#
#     def add(self, product, quantity=1, replace_current_quantity=False):
#         """
#         Add the specified product to the cart if it exists
#         """
#         product_id = str(product.id)
#
#         if product_id not in self.cart:
#             self.cart[product_id] = {'quantity': 0}
#
#         if replace_current_quantity:
#             self.cart[product_id]['quantity'] = quantity
#         else:
#             self.cart[product_id]['quantity'] += quantity
#
#         messages.success(self.request, _('Product successfully added to cart'))
#
#         self.save()
#
#     def remove(self, product):
#         """
#         Remove a product from the cart
#         """
#         product_id = str(product.id)
#
#         if product_id in self.cart:
#             del self.cart[product_id]
#             messages.success(self.request, _('Product successfully removed from cart'))
#             self.save()
#
#     def save(self):
#         """
#         Mark session as modified to save changes
#         """
#         self.session.modified = True
#
#     def __iter__(self):
#         cart = self.cart
#         if cart:
#             product_ids = cart.keys()
#             products = Package.objects.filter(id__in=product_ids)
#             if len(products) > 0:
#                 for product in products:
#                     cart[str(product.id)]['product_obj'] = product
#
#                 for item in cart.values():
#                     item['total_price'] = item['product_obj'].price * item['quantity']
#                     yield item
#
#     def __len__(self):
#         """    GET LENGTH OF CART  """
#
#         print('im in len')
#         # return len(self.cart.keys()) its show only product length without quantity
#         return sum(item['quantity'] for item in self.update().values())
#
#     def clear(self):
#         del self.session['cart']
#         self.save()
#
#     def get_total_price(self):
#         cart = self.cart
#         cart.update()
#         product_ids = cart.keys()
#         if len(product_ids) > 0:
#             return sum(item['quantity'] * item['product_obj'].price for item in self.cart.values())
#
#     def is_empty(self):
#         if self.cart:
#             return False
#         return True
#
#     def update(self):
#         cart = self.cart
#         print('************im in update')
#         if cart:
#             print('************im in if')
#
#             for id_product in cart.keys():
#                 product = Package.objects.filter(id=id_product)
#                 print(product)
#                 if not product:
#                     cart.pop(id_product)
#                     self.save()
#                     print('*****************im in update and not product')
#
#             if cart.keys() == 0:
#                 print('*******************im in update after not product')
#                 self.clear()
#                 self.save()
#                 return not cart
#
#             return cart


from django.utils.translation import gettext as _
from django.contrib import messages

from pages.models import Package


class Cart:
    def __init__(self, request):
        """
        Initialize the cart
        """
        self.request = request

        self.session = request.session

        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart

    def add(self, product, quantity=1, replace_current_quantity=False):
        """
        Add the specified product to the cart if it exists
        """
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0}

        if replace_current_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        messages.success(self.request, _('Product successfully added to cart'))

        self.save()

    def remove(self, product):
        """
        Remove a product from the cart
        """
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            messages.success(self.request, _('Product successfully removed from cart'))
            self.save()

    def save(self):
        """
        Mark session as modified to save changes
        """
        self.session.modified = True

    def __iter__(self):
        cart = self.cart
        print('************im in update')

        for id_product in cart.keys():
            product = Package.objects.filter(id=id_product)
            print(product)
            if not product:
                cart.pop(id_product)
                self.save()
                print('*****************im in update and not product')
        if cart.keys():
            print('************im in if')

            product_ids = cart.keys()
            products = Package.objects.filter(id__in=product_ids)

            # cart = self.cart.copy()

            for product in products:
                cart[str(product.id)]['product_obj'] = product

            for item in cart.values():
                item['total_price'] = item['product_obj'].price * item['quantity']
                yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session['cart']
        self.save()

    def get_total_price(self):
        product_ids = self.cart.keys()

        return sum(item['quantity'] * item['product_obj'].price for item in self.cart.values())

    def is_empty(self):
        if self.cart:
            return False
        return True