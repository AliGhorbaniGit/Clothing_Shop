from django.db import models
from django.utils.translation import gettext as _

from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField


class Order(models.Model):
    """ CREATE A MODEL TO SAVE ORDER"""

    class Meta:
        verbose_name = _("Orders")
        verbose_name_plural = _("Orders")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_order', on_delete=models.CASCADE,
                             verbose_name=_('user'))
    # when I have this in setting, so I can use this variable here
    is_paid = models.BooleanField(default=False, verbose_name=_('is paid'))

    first_name = models.CharField(max_length=100, verbose_name=_('first_name'))
    last_name = models.CharField(max_length=100, verbose_name=_('last_name'))
    phone_number = PhoneNumberField(verbose_name=_('phone_number'))
    address = models.CharField(max_length=700, verbose_name=_('address'))

    order_notes = models.CharField(max_length=700, blank=True)

    zarinpal_authority = models.CharField(max_length=255, blank=True)
    zarinpal_ref_id = models.CharField(max_length=150, blank=True)
    zarinpal_data = models.TextField(blank=True)

    data_created = models.DateTimeField(auto_now_add=True, verbose_name=_("data_created"))
    data_modified = models.DateTimeField(auto_now=True, verbose_name=_("data_modified"))

    def __str__(self):
        return f'Order {self.id}'

    def get_total_price(self):
        """ GET TOTAL PRICE OF ORDER """
        result = 0
        for item in self.items.all():
            """ here self is this order its equal to write order.items, its a query """
            result += item.price * item.quantity
            return result
        """ I can write that code in one line: return sum(item.price * item.quantity for item in self.items.all()) """


class OrderItem(models.Model):
    """ CREATE A MODEL TO SAVE ITEMS OF ORDER """

    class Meta:
        verbose_name = _("OrderItems")
        verbose_name_plural = _("OrderItems")

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_('which order'))
    product = models.ForeignKey('pages.package', on_delete=models.CASCADE, related_name='order_items',
                                verbose_name=_('which product'))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('quantity'))
    price = models.PositiveIntegerField(verbose_name=_('price'))

    def __str__(self):
        return f'OrderItem {self.id}:{self.product} x {self.quantity} (price:{self.price}) of oder {self.order.id}'
