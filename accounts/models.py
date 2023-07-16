from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True, verbose_name=_('username'))
    password = models.CharField(verbose_name=_('password'))
    email = models.EmailField(blank=True, verbose_name=_('email'))
    number = PhoneNumberField(blank=True, verbose_name=_('number') )
    is_staff = models.BooleanField(default=False, verbose_name=_('is_staff'))
    data_joined = models.DateTimeField(auto_now_add=True, verbose_name=_('data_joined'))

    def get_absolute_url(self):
        return reverse('ShowPackages')
