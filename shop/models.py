from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

from accounts.models import CustomUser


class Product(models.Model):
    """ THIS IS THE PRODUCT MODEL  """

    class Meta:
        verbose_name = _("PRODUCT")
        verbose_name_plural = _("PRODUCTS")

    title = models.CharField(max_length=200, verbose_name=_('Title'))
    price = models.IntegerField(verbose_name=_('Price'))
    image = models.ImageField(blank=True, upload_to='image/products_image', verbose_name=_('Image'))
    material = models.CharField(max_length=100, blank=True, verbose_name=_('Material'))
    description = RichTextField(blank=True, verbose_name=_('Description'))
    is_offer = models.BooleanField(default=False, verbose_name=_('Offer'))
    offer_percent = models.PositiveIntegerField(default=0, verbose_name='Offer Percent')
    show = models.BooleanField(default=False, verbose_name=_('Show'))
    available = models.BooleanField(default=True, verbose_name=_('Available'))
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_('date created'))
    datetime_modified = models.DateTimeField(auto_now=True, verbose_name=_('date modified'))

    def price_by_offer(self):
        if self.is_offer:
            return int(self.price - ((self.price * self.offer_percent) / 100))
        else:
            return int(self.price)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.pk])


class ProductColorSizeCount(models.Model):
    """     THIS MODEL GET THE SIZE COLOR AND COUNT OF PRODUCT      """

    class Meta:
        verbose_name = _("product's Size AND Color")
        verbose_name_plural = _("Products Size And Color  ")

    size_CHOICES = (
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
    )

    product = models.ForeignKey(Product, related_name='size_color_count',
                                on_delete=models.CASCADE, verbose_name=_("Product"))

    size = models.CharField(max_length=8, choices=size_CHOICES, verbose_name=_('Product Size'))

    color_1 = models.CharField(max_length=30, verbose_name=_('color 1'), )
    how_many_color_1 = models.PositiveIntegerField(default=0, verbose_name=_('How many color 1'))

    color_2 = models.CharField(blank=True, max_length=30, verbose_name=_('color 2'), )
    how_many_color_2 = models.PositiveIntegerField(default=0, verbose_name=_('How many color 2'))

    color_3 = models.CharField(blank=True, max_length=30, verbose_name=_('color 3'), )
    how_many_color_3 = models.PositiveIntegerField(default=0, verbose_name=_('How many color 3'))

    color_4 = models.CharField(blank=True, max_length=100, verbose_name=_('color 4'), )
    how_many_color_4 = models.PositiveIntegerField(default=0, verbose_name=_('How many 4'))

    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_('date created'))
    datetime_modified = models.DateTimeField(auto_now=True, verbose_name=_('date modified'))


class Comment(models.Model):
    """     THIS IS THE COMMENT MODEL   """

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    author = models.ForeignKey(get_user_model(), related_name='comments', on_delete=models.CASCADE,
                               verbose_name=_("author"))
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE,
                                verbose_name=_('product'))
    text = models.TextField(verbose_name=_("text"))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_("date created"))
    date_modified = models.DateTimeField(auto_now=True, verbose_name=_("date modified"))

    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.product.id])


class ReplyComment(models.Model):
    """     THIS IS A MODEL FOR EVERY REPLY OF COMMENT   """

    class Meta:
        verbose_name = _("ReplyComment")
        verbose_name_plural = _("ReplyComments")

    reply_author = models.ForeignKey(CustomUser, related_name='reply', on_delete=models.CASCADE,
                                     verbose_name=_("reply author"))
    reply_product = models.ForeignKey(Product, related_name='reply', on_delete=models.CASCADE,
                                      verbose_name=_('reply product'))
    reply_comment = models.ForeignKey(Comment, related_name='reply', on_delete=models.CASCADE,
                                      verbose_name=_("reply comment "))
    text = models.TextField(verbose_name=_("text"))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_("date created"))
    date_modified = models.DateTimeField(auto_now=True, verbose_name=_("date modified"))

    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.reply_product.pk])


class AdminAwareness(models.Model):
    date_time_sent = models.DateTimeField(auto_now_add=True, verbose_name=_("send date time"))
    date_time_seen = models.DateTimeField(auto_now=True, verbose_name=_("seen date time"))
    sender = models.CharField(max_length=50, verbose_name=_("sender"))
    subject = models.CharField(max_length=300, verbose_name=_("subject"))
    access_way = models.CharField(max_length=100, verbose_name=_("access way"))
    is_checked = models.BooleanField(default=False, verbose_name=_("is checked ?"))
