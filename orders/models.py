from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from shop.models import Product


class Order(models.Model):
    """     CREATE A MODEL TO STORE ORDERS    """

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    user = models.ForeignKey(get_user_model(), related_name='orders', on_delete=models.CASCADE,
                             verbose_name=_('User'))
    is_paid = models.BooleanField(default=False, verbose_name=_('Is Paid'))
    first_name = models.CharField(max_length=25, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=25, verbose_name=_('Last Name'))

    phone_number = models.PositiveIntegerField(verbose_name=_('Phone Number'))
    address = models.CharField(max_length=600, verbose_name=_('Address'))
    order_notes = models.CharField(max_length=700, blank=True, verbose_name=_('Order Notes'))

    zarinpal_authority = models.CharField(max_length=255, blank=True, verbose_name=_('Zarinpal Authority'))
    zarinpal_ref_id = models.CharField(max_length=150, blank=True, verbose_name=_('Zarinpal Ref Id'))
    zarinpal_data = models.TextField(blank=True, verbose_name=_('Zarinpal Data'))

    date_time_created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    date_time_modified = models.DateTimeField(auto_now=True, verbose_name=_("Modified at"))

    def __str__(self):
        return f'Order {self.id} , paid : {self.is_paid}'

    def get_total_price(self):
        """ GET TOTAL PRICE OF ORDER """
        result = 0
        for item in self.items.all():
            result += item.price * item.quantity
            return result


class OrderItem(models.Model):
    """ STORE ORDER ITEMS """

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_('Order'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='Order_items',
                                verbose_name=_('Product'))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('Quantity'))
    color = models.CharField(max_length=20, verbose_name=_('Color'))
    size = models.CharField(max_length=20, verbose_name=_('Size'))
    price = models.PositiveIntegerField(verbose_name=_('Price'))

    def __str__(self):
        return f'Order Item {self.id}: {self.product.title} x {self.quantity} '
