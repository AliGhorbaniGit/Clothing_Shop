from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.utils.translation import gettext as _
from django.contrib import messages

from cart.cart import Cart
from .favorite import Favorite
from .forms import AddToCartForm
from pages.models import Package


def cart_detail_view(request):
    print('in first')
    cart = Cart(request)
    print('in second')
    if cart.is_empty():
        print('in third')
        for item in cart:
            item['product_update_quantity_form'] = AddToCartForm(initial={
                'quantity': item['quantity'],
                'inplace': True,
            })
        print('there is cart')
        print()
        return render(request, 'cart/cart_detail.html', {'cart': cart})
    else:
        print('the products that you added , now deleted ')
        return render(request, 'cart/cart_detail.html')


# def cart_detail_view(request):
#
#     cart = Cart(request)
#     for item in cart:
#         pass
#
#     if cart:
#         for item in cart:
#             item['product_update_quantity_form'] = AddToCartForm(initial={
#                 'quantity': item['quantity'],
#                 'inplace': True,
#             })
#             return render(request, 'cart/cart_detail.html', {'cart': cart, })
#     else:
#         messages.warning(request, 'your cart is empty , or the products that you had added , already not')
#         return render(request, 'cart/cart_detail.html', )
#

def add_to_cart_view(request, product_id):
    print('im in add to cart view')
    cart = Cart(request)
    print('i am after cart')
    product = get_object_or_404(Package, id=product_id)
    print('i am after product')
    form = AddToCartForm(request.POST)
    print('i am after from')
    if form.is_valid():
        print('the form is valid')
        cleaned_data = form.cleaned_data
        quantity = cleaned_data['quantity']
        replace_current_quantity = cleaned_data['inplace']
        cart.add(product, quantity, replace_current_quantity)
        print('form is valid product added')
    print('im go to return')
    return redirect('cart:cart_detail')


def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Package, id=product_id)

    cart.remove(product)

    return redirect('cart_detail')


def clear_cart(request):
    cart = Cart(request)

    if len(cart):
        cart.clear()
        messages.success(request, _('your cart get empy'))
    else:
        messages.warning(request, _('you have nothing in cart'))
    return redirect('cart:cart_detail')


def add_to_favorites(request, product_id):
    # if user is authnrticated
    #     stote in db
    # else
    #     stote in session
    favorite = Favorite(request)

    favorite.add(product_id)
    return redirect('ShowPackages')


def favorites_list(request):
    favorite = Favorite(request)
    if favorite.is_empty() or False:
        messages.success(request, _('your wish list is empty '))
        return redirect('ShowPackages')
    # favorite.clear()
    # favorite.save()
    product_ids = favorite
    favorites = Package.objects.filter(id__in=product_ids)

    return render(request, 'pages/wishlist.html', {'favorites': favorites})
