from django.db import models
from django.utils.translation import gettext as _

from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'))
    # when I have this in setting, so I can use this variable here
    is_paid = models.BooleanField(default=False, verbose_name=_('is paid'))

    first_name = models.CharField(max_length=100, verbose_name=_('first_name'))
    last_name = models.CharField(max_length=100, verbose_name=_('last_name'))
    phone_number = PhoneNumberField(verbose_name=_('phone_number'))
    address = models.CharField(max_length=700, verbose_name=_('address'))

    order_notes = models.CharField(max_length=700, blank=True)

    data_created = models.DateTimeField(auto_now_add=True, verbose_name=_("data_created"))
    data_modified = models.DateTimeField(auto_now=True, verbose_name=_("data_modified"))

    def __str__(self):
        return f'Order {self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('pages.package', on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f'OrderItem {self.id}:{self.product} x {self.quantity} (price:{self.price}) of oder {self.order.id}'
