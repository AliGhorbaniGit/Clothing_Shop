from copy import deepcopy
from django.utils.translation import gettext as _
from django.contrib import messages

from shop.models import Product


class Favorite:
    def __init__(self, request):
        """    Initialize the Favorite  """

        self.request = request
        self.session = request.session

        favorites = self.session.get('favorites')

        if not favorites:
            favorites = self.session['favorites'] = {}

        self.favorites = favorites

    def add(self, product_id):
        """    Add the specified product to the Favorite if it exists     """

        if product_id not in self.favorites.values():
            self.favorites[product_id] = product_id
            messages.success(self.request, _('Product successfully added to your favorite'))

        else:
            product_id = str(product_id)
            del self.favorites[product_id]
            messages.success(self.request, _('Product successfully removed from your wish list'))

        self.save()

    def save(self):
        """   Mark session as modified to save changes   """
        self.session.modified = True

    def __iter__(self):
        """ make the Favorite iterable   """

        favorites = deepcopy(self.favorites)

        for id_product in favorites:
            product = Product.objects.filter(id=id_product)
            if product:
                pass

            else:
                del self.favorites[str(id_product)]
                self.save()

        product_ids = favorites.values()

        for item in product_ids:
            yield item

    def __len__(self):

        favorites = self.favorites
        if favorites:
            return len(favorites)
        else:
            return False

    def clear(self):
        del self.session['favorites']
        self.save()

    def is_empty(self):
        if self.favorites:
            return False
        return True
