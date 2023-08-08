from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.utils.translation import gettext as _
from django.contrib import messages

from cart.cart import Cart
from .forms import AddToCartForm
from pages.models import Package


# def cart_detail_view(request):
#     cart = Cart(request)
#     fresh_cart = cart.__iter__()
#     if fresh_cart :
#         for item in fresh_cart:
#             item['product_update_quantity_form'] = AddToCartForm(initial={
#                 'quantity': item['quantity'],
#                 'inplace': True,
#             })
#         return render(request, 'cart/cart_detail.html', {'cart': fresh_cart})
#     else:
#         messages.warning(request, 'the products that you added , now deleted ')
#         return render(request, 'cart/cart_detail.html')

def cart_detail_view(request):
    cart = Cart(request)
    # cart.update()
    print('**********im in after')
    if cart:
        for item in cart:
            item['product_update_quantity_form'] = AddToCartForm(initial={
                'quantity': item['quantity'],
                'inplace': True,
            })
            print('******* im here in cart_detail_view(request):')
            return render(request, 'cart/cart_detail.html', {'cart': cart, })
    else:
        print('******* not cart, im here in cart_detail_view(request):')
        return render(request, 'cart/cart_detail.html', )


def add_to_cart_view(request, product_id):
    cart = Cart(request)

    product = get_object_or_404(Package, id=product_id)
    form = AddToCartForm(request.POST)

    if form.is_valid():
        cleaned_data = form.cleaned_data
        quantity = cleaned_data['quantity']
        replace_current_quantity = cleaned_data['inplace']
        cart.add(product, quantity, replace_current_quantity)

    return redirect('cart_detail')


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
    return redirect('cart_detail')
