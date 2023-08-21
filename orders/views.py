from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _

from .forms import OrderForm
from .models import OrderItem

from cart.cart import Cart


@login_required
def order_create_view(request):
    order_form = OrderForm()
    cart = Cart(request)
    cart = Cart(request)
    print('*********************im in create order')
    if len(cart) == 0:
        print('*****************im in create order and len cart is 0')
        messages.warning(request, _('u must add some product first'))
        return redirect('ShowPackages')
    if request.method == 'POST':
        print('in in not len')
        order_form = OrderForm(request.POST)
        print('*******************in request.method == post')
        if order_form.is_valid():
            order_obj = order_form.save(commit=False)
            order_obj.user = request.user
            order_obj.save()

            for item in cart:
                product = item['product_obj']
                OrderItem.objects.create(
                    order=order_obj,
                    product=product,
                    quantity=item['quantity'],
                    price=product.price,
                )
            # cart.clear()

            request.user.first_name = order_obj.first_name
            request.user.last_name = order_obj.last_name
            request.user.save()
            messages.success(request, _('your order has successfully add'))

            request.session['order_id'] = order_obj.id
            print('payment is ok')
            return redirect('payment_process')

    return render(request, 'orders/order_create.html',
                  {'order_form': order_form, })
