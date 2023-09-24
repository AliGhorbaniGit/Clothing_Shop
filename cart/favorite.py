from django.utils.translation import gettext as _
from django.contrib import messages

from pages.models import Package


class Favorite:
    def __init__(self, request):
        """    Initialize the cart  """

        self.request = request

        self.session = request.session

        favorites = self.session.get('favorites')

        if not favorites:
            favorites = self.session['favorites'] = {}

        self.favorites = favorites

    def add(self, product_id):
        """    Add the specified product to the cart if it exists     """

        product_id = str(product_id)

        if product_id not in self.favorites:
            self.favorites[product_id] = product_id
            print('in add 1')
            messages.success(self.request, _('Product successfully added to your favorite'))

        else:
            print('in add 3')
            messages.success(self.request, _('Product already exists'))


        self.save()


    def save(self):
        """   Mark session as modified to save changes   """

        self.session.modified = True
    #
    #
    # def remove(self, product_id):
    #     """    Remove a product from the cart    """
    #
    #     product_id = str(product_id)
    #
    #     if product_id in self.favorites:
    #         del self.favorites[product_id]
    #         messages.success(self.request, _('Product successfully removed from cart'))
    #         self.save()
    #
    #
    # def __iter__(self):
    #     """ make the cart iterable   """
    #
    #     """ i can get :  cart = self.cart.copy()
    #     I don't want to change the cart
    #     so I copy it because when I copy
    #     a things, the main don't change,
    #     here self.cart will never change, and cart will change    """
    #     favorites = self.favorites
    #     print('im in iter')
    #     for id_product in favorites:
    #         print('im in iter and for')
    #
    #         product = Package.objects.filter(id=id_product)
    #
    #         if product:
    #             pass
    #             print('there is this product')
    #         else:
    #             # cart.pop(__key=product)
    #             del favorites.id_product
    #             print('there i not this product')
    #             self.save()
    #             break
    #
    #         # if len(cart.keys())==0:
    #         #     messages.warning(self.request, f"im in len/for/if{len(cart.keys())}")
    #         #
    #         #     self.clear()
    #         #     self.save()
    #         #     return False
    #
    #     product_ids = favorites
    #     products = Package.objects.filter(id__in=product_ids)
    #
    #     for item in favorites.values():
    #         yield item
    #
    # def __len__(self):
    #     print('im in len')
    #     favorites = self.favorites
    #     if favorites:
    #         print('###################### in len there is cart')
    #         return sum(item['quantity'] for item in self.favorites.values())
    #     else:
    #         print('#######################in len there is no cart')
    #         return False
    #
    # #             return sum(item['quantity'] * item['product_obj'].price for item in self.cart.values())
    # #         # return len(self.cart.keys()) its show only product length without quantity
    # #         return sum(item['quantity'] for item in self.update().values())
    # #
    # def clear(self):
    #     del self.session['favorites']
    #     self.save()
    #
    # def is_empty(self):
    #     if self.favorites:
    #         return False
    #     return True
