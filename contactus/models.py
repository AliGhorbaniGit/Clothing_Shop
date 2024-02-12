from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


class ContactUs(models.Model):
    """     stores the user and admin conversation as 'contact us'     """

    class Meta:
        verbose_name = _("Contact Us")
        verbose_name_plural = _("Contacts Us")

    user = models.ForeignKey(get_user_model(), related_name='contactus',
                             on_delete=models.CASCADE, verbose_name=_("User Name"))
    user_text = models.TextField(_('user message'), max_length='255', )
    admin_text = models.TextField(_('admin message'), blank=True, max_length='255', )
    is_new = models.BooleanField(default=True, verbose_name=_('new'))
    user_sent_date_time = models.TimeField(auto_now_add=True, verbose_name=_('send at'))
    admin_sent_date_time = models.TimeField(auto_now=True, verbose_name=_('answers at'))

    def get_absolute_url(self):
        return reverse('contactus:all_new_contact')
