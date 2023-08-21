from django.utils.translation import gettext as _
from django.contrib import messages

from pages.models import Package


class Cart:
    def __init__(self, request):
        """    Initialize the cart  """

        self.request = request

        self.session = request.session

        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart

    def add(self, product, quantity=1, replace_current_quantity=False):
        """    Add the specified product to the cart if it exists     """

        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': quantity}
            print('in add 1')
        elif replace_current_quantity:
            print('in add 2')
            self.cart[product_id]['quantity'] = quantity
        else:
            print('in add 3')
            self.cart[product_id]['quantity'] += quantity

        messages.success(self.request, _('Product successfully added to your cart'))

        self.save()

    def remove(self, product):
        """    Remove a product from the cart    """

        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            messages.success(self.request, _('Product successfully removed from cart'))
            self.save()

    def save(self):
        """   Mark session as modified to save changes   """

        self.session.modified = True

    def __iter__(self):
        """ make the cart iterable   """

        """ i can get :  cart = self.cart.copy()  
        I don't want to change the cart 
        so I copy it because when I copy
        a things, the main don't change,
        here self.cart will never change, and cart will change    """
        cart = self.cart
        print('im in iter')
        for id_product in cart.keys():
            print('im in iter and for')

            product = Package.objects.filter(id=id_product)

            if product:
                pass
                print('there is this product')
            else:
                # cart.pop(__key=product)
                del cart[str(id_product)]
                print('there i not this product')
                self.save()
                break

            # if len(cart.keys())==0:
            #     messages.warning(self.request, f"im in len/for/if{len(cart.keys())}")
            #
            #     self.clear()
            #     self.save()
            #     return False

        product_ids = cart.keys()
        products = Package.objects.filter(id__in=product_ids)

        for product in products:
            cart[str(product.id)]['product_obj'] = product

        for item in cart.values():
            item['total_price'] = item['product_obj'].price * item['quantity']
            yield item

    def __len__(self):
        print('im in len')
        cart = self.cart
        if cart:
            print('###################### in len there is cart')
            return sum(item['quantity'] for item in self.cart.values())
        else:
            print('#######################in len there is no cart')
            return False

    #             return sum(item['quantity'] * item['product_obj'].price for item in self.cart.values())
    #         # return len(self.cart.keys()) its show only product length without quantity
    #         return sum(item['quantity'] for item in self.update().values())
    #
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
