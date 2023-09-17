from django.contrib import auth
from django.db import models
from accounts.models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


class Contact(models.Model):
    pass


#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
#                              related_name='user_name', verbose_name=_('user'))
#     user_text = models.TextField(_('user_text'))
#     admin_text = models.TextField(_('admin_text'), blank=True, )
#     datetime_user_created = models.TimeField(auto_now_add=True, verbose_name=_('datetime_user_created'))
#     datetime_admin_created = models.TimeField(auto_now_add=True, verbose_name=_('datetime_admin_created'))
#
#
# class ContactContext(models.Model):
#     # user_name = models.ForeignKey(Contact, on_delete=models.CASCADE,
#     #                               , verbose_name=_('user_name'))
#     user_text = models.TextField(_('user_text'))
#     admin_text = models.TextField(_('admin_text'), blank=True, )
#     datetime_user_created = models.TimeField(auto_now_add=True, verbose_name=_('datetime_user_created'))
#     datetime_admin_created = models.TimeField(auto_now_add=True, verbose_name=_('datetime_admin_created'))


class ContactUs(models.Model):
    user = models.ForeignKey(CustomUser, related_name='contact_us', on_delete=models.CASCADE, verbose_name=_("user"))
    user_text = models.TextField(_('user_text'))
    admin_text = models.TextField(_('admin_text'), blank=True, )
    datetime_user_created = models.TimeField(auto_now_add=True, verbose_name=_('datetime_user_created'))
    # datetime_admin_created = models.TimeField(auto_now_add=True, verbose_name=_('datetime_admin_created'),default=None)
