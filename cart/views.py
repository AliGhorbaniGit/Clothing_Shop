from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.utils.translation import gettext as _
from django.contrib import messages

from cart.cart import Cart
from .favorite import Favorite
from .forms import AddToCartForm
from shop.models import Product


@require_POST
def add_to_cart_view(request, product_id):
    """ GET ID, COLOR, SIZE AND QUANTITY OF A PRODUCT FROM ADD FORM TO BE ADDED TO CART"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = AddToCartForm(request.POST)

    if form.is_valid():
        cleaned_data = form.cleaned_data
        quantity = cleaned_data['quantity']
        color = cleaned_data['color']
        size = cleaned_data['size']
        replace_current_quantity = False

        cart.add(product, size, color, quantity, replace_current_quantity)
    else:
        messages.warning(request, 'Oops , did you forgot to choose size and color !!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def cart_detail_view(request):
    """ SHOW CART DETAIL """

    cart = Cart(request)
    for item in cart:
        item['product_update_quantity_form'] = AddToCartForm(initial={
            'quantity': item['quantity'],
            'inplace': True,
        })
    return render(request, 'cart/cart_detail.html', {
        'cart': cart,
    })


def remove_from_cart(request, product_id):
    """ REMOVE AN ID FROM CART  """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def clear_cart(request):
    """ CLEAR CART FROM SESSION """
    cart = Cart(request)

    if cart.is_empty():
        messages.warning(request, _('you have nothing in cart'))

    else:
        cart.clear()
        messages.success(request, _('your cart get empy'))

    return redirect('cart:cart_detail')



def add_to_favorites(request, product_id):
    """ add/remove , to/from favorite """
    get_object_or_404(Product, id=product_id)
    favorite = Favorite(request)
    favorite.add(product_id)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def favorites_list(request):
    favorite = Favorite(request)
    if favorite.is_empty() or False:
        messages.success(request, _('your favorites list is empty '))

    product_ids = favorite
    favorites = Product.objects.filter(id__in=product_ids)

    return render(request, 'shop/product_list.html', {'products': favorites})
