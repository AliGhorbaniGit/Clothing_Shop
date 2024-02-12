from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.utils.translation import gettext as _

from cart.cart import Cart
from .forms import OrderForm
from .models import OrderItem


@login_required
def order_create_view(request):
    order_form = OrderForm()
    cart = Cart(request)

    if len(cart) == 0:
        messages.warning(request, _('You can not proceed to checkout page because your cart is empty.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if request.method == 'POST':
        order_form = OrderForm(request.POST, )

        if order_form.is_valid():
            order_obj = order_form.save(commit=False)
            order_obj.user = request.user
            order_obj.save()

            for item in cart:
                product = item['product_obj']
                if product.available:
                    # CHECK THAT IS THERE PRODUCT QUANTITY MORE THAT USER ORDER OR NOT
                    how_many = 1
                    targets = product.size_color_count.all()
                    for target in targets:
                        if target.color_1 == item['color']:
                            how_many = target.how_many_color_1

                        elif target.color_2 == item['color']:
                            how_many = target.how_many_color_2

                        elif target.color_3 == item['color']:
                            how_many = target.how_many_color_3

                        elif target.color_4 == item['color']:
                            how_many = target.how_many_color_4

                        else:
                            messages.error(request, f"You Choose color : {item['color']} "
                                                    f"for product : {product.title} "
                                                    f"that not exists , please Choose another color")
                            return reverse('shop:product_detail', args=[product.id])

                        if item['quantity'] > how_many:
                            messages.error(request, f"You Choose color : {item['color']} "
                                                    f"for product : {product.title} "
                                                    f"with : {how_many} count "
                                                    f"that already dose unavailable , please Choose {how_many} count or less ")
                            return reverse('shop:product_detail', args=[product.id])

                    OrderItem.objects.create(
                        order=order_obj,
                        product=product,
                        quantity=item['quantity'],
                        size=item['size'],
                        color=item['color'],
                        price=product.price,
                    )

                # else:
                #     del cart[str(product.id)]
                #     cart.save()

            request.user.first_name = order_obj.first_name
            request.user.last_name = order_obj.last_name
            request.user.save()

            request.session['order_id'] = order_obj.id
            return redirect('payments:payment_process')

    return render(request, 'orders/order_create.html', {
        'form': order_form,
    })
