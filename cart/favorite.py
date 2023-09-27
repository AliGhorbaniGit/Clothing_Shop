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

        if product_id not in self.favorites.values():
            self.favorites[product_id] = product_id
            print('in add 1')
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
        """ make the cart iterable   """
        favorites = self.favorites
        print('im in iter')
        for id_product in favorites:
            print('im in iter and for')

            product = Package.objects.filter(id=id_product)

            if product:
                pass

            else:
                product_id = str(id_product)
                del self.favorites[product_id]
                self.save()
                break

            if len(favorites.keys()) == 0:
                self.clear()
                self.save()
                return False

        product_ids = favorites.values()

        for item in product_ids:
            yield item

    def __len__(self):
        print('im in len')
        favorites = self.favorites
        if favorites:
            return len(favorites)
        else:
            print('#######################in len there is no cart')
            return False

    def clear(self):
        del self.session['favorites']
        self.save()

    def is_empty(self):
        if self.favorites:
            return False
        return True
