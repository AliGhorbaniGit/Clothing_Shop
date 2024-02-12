import requests
import json

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, reverse
from django.http import HttpResponse
from django.utils.translation import gettext as _

from django.conf import settings

from orders.models import Order, OrderItem
from shop.models import Product, ProductColorSizeCount
from cart.cart import Cart


def payment_process(request):
    # GET ORDER ID FROM SESSION :
    order_id = request.session.get('order_id')
    # GET THE ORDER OBJECT
    order = get_object_or_404(Order, id=order_id)

    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    zarinpal_request_url = 'https://api.zarinpal.com/pg/v4/payment/request.json'

    request_header = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    request_data = {
        'merchant_id': settings.ZARINPAL_MERCHANT_ID,
        'amount': rial_total_price,
        'description': f'#{order.id}: {order.user.first_name} {order.user.last_name}',
        'callback_url': 'http://127.0.0.1:8000' + reverse('payments:payment_callback')
        # this is one way but not professional :
        # '127.0.0.1:8000' + reverse('payment_callback'),

    }
    res = requests.post(url=zarinpal_request_url, data=json.dumps(request_data), headers=request_header)
    data = res.json()['data']
    authority = data['authority']
    order.zarinpal_authority = authority
    order.save()

    if 'errors' not in data or len(data['errors']) == 0:
        return redirect(f'https://www.zarinpal.com/pg/StartPay/{authority}')
    else:
        messages.error(request, message=_('error occurred'))
        return HttpResponse(_(f'this error occurred :{data.errors}'))


def payment_callback(request):
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get('Status')

    order = get_object_or_404(Order, zarinpal_authority=payment_authority)
    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    if payment_status == 'OK':
        request_header = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        request_data = {
            'merchant_id': settings.ZARINPAL_MERCHANT_ID,
            'amount': rial_total_price,
            'authority': payment_authority
        }

        res = requests.post(
            url='https://api.zarinpal.com/pg/v4/payment/verify.json',
            data=json.dumps(request_data),
            headers=request_header,
        )

        if 'data' in res.json() and ('errors' not in res.json()['data'] or len(res.json()['data']['errors']) == 0):
            data = res.json()['data']
            payment_code = data['code']

            if payment_code == 100:
                order.is_paid = True
                order.ref_id = data['ref_id']
                order.zarinpal_data = data
                order.save()

                # clearing cart
                cart = Cart(request)
                cart.clear()

                # update product quantity at data base
                order_items = order.items.all()
                for order in order_items:
                    products = Product.objects.filter(id=order.product.id)
                    for product in products:
                        target_product = product.size_color_count.all()

                        for target in target_product:

                            if target.color_1 == order.color:
                                if target.how_many_color_1 >= order.quantity:
                                    updated = target.how_many_color_1 - order.quantity
                                    ProductColorSizeCount.objects.filter(pk=target.id).update(how_many_color_1=updated)
                                else:
                                    ProductColorSizeCount.objects.filter(pk=target.id).update(how_many_color_1=0)

                            elif target.color_2 == order.color:
                                if target.how_many_color_2 >= order.quantity:
                                    updated = target.how_many_color_2 - order.quantity
                                    ProductColorSizeCount.objects.filter(pk=target.id).update(how_many_color_2=updated)
                                else:
                                    ProductColorSizeCount.objects.filter(pk=target.id).update(how_many_color_1=0)

                            elif target.color_3 == order.color:
                                if target.how_many_color_3 >= order.quantity:
                                    updated = target.how_many_color_3 - order.quantity
                                    ProductColorSizeCount.objects.filter(pk=target.id).update(how_many_color_3=updated)
                                else:
                                    ProductColorSizeCount.objects.filter(pk=target.id).update(how_many_color_1=0)

                            elif target.color_4 == order.color:
                                if target.how_many_color_4 >= order.quantity:
                                    updated = target.how_many_color_4 - order.quantity
                                    ProductColorSizeCount.objects.filter(pk=target.id).update(how_many_color_4=updated)
                                else:
                                    ProductColorSizeCount.objects.filter(pk=target.id).update(how_many_color_1=0)

                            # if (
                            #         target.how_many_color_1 and target.how_many_color_2 and target.how_many_color_3 and target.how_many_color_4) == 0:
                            #     Product.objects.filter(pk=product.id).update(available=False)

                            if all(getattr(target, f'how_many_color_{i}') == 0 for i in range(1, 5)):
                                Product.objects.filter(pk=target.product.id).update(available=False)

                return HttpResponse(
                    _('your payment process was successful'))  # it's better to use a template for message

            elif payment_code == 101:
                return HttpResponse(_('this payment was successful and submitted in past '))

            else:
                error_code = res.json()['errors']['code']
                error_message = res.json()['errors']['message']

                return HttpResponse(_(f'{error_code} : {error_message} : unsuccessful'))

    else:
        return HttpResponse(_(' unsuccessful'))

#
# def product_quantity_update(request):
#     user = request.user
#     orders = user.orders.all()
#     color_fields = ['color_1', 'color_2', 'color_3', 'color_4']
#
#     for order in orders:
#         for orderr in order.items.last():
#             products = Product.objects.filter(id=orderr.product.id)
#             for product in products:
#                 target_product = product.size_color_count.all()
#                 for target in target_product:
#
#                     if target.color_1 == orderr.color and target.how_many_color_1 > 0:
#                         updated = target.how_many_color_1 - orderr.quantity
#                         ProductColorSizeCount.objects.filter(pk=target.id).update(how_many_color_1=updated)
#
#                     elif target.color_2 == orderr.color and target.how_many_color_2 > 0:
#                         updated = target.how_many_color_2 - orderr.quantity
#                         ProductColorSizeCount.objects.filter(pk=target.id).update(how_many_color_2=updated)
#
#                     elif target.color_3 == orderr.color and target.how_many_color_3 > 0:
#                         updated = target.how_many_color_3 - orderr.quantity
#                         ProductColorSizeCount.objects.filter(pk=target.id).update(how_many_color_3=updated)
#
#                     elif target.color_4 == orderr.color and target.how_many_color_4 > 0:
#                         updated = target.how_many_color_4 - orderr.quantity
#                         ProductColorSizeCount.objects.filter(pk=target.id).update(how_many_color_4=updated)
#
#                     else:
#                         messages.warning(request, 'it seems some strange things happen')
