from urllib import request
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """ this model make user fields editable"""
    number = models.IntegerField(null=True, blank=True, error_messages='', verbose_name=_('Phone Number'))
    image = models.ImageField(blank=True, upload_to='image/users_image', verbose_name=_('Image'))

    def get_absolute_url(self):
        return redirect(request.GET.get('next', '/'))
