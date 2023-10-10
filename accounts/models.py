from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True, verbose_name=_('User Name'))
    first_name = models.CharField(max_length=30, blank=True, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=30, blank=True, verbose_name=_('Last Name'))
    password = models.CharField(verbose_name=_('Password'))
    email = models.EmailField(verbose_name=_('Email'))
    # number = PhoneNumberField(blank=True, verbose_name=_('Phone Number'))
    number = models.IntegerField(blank=True, verbose_name=_('Phone Number'))
    is_staff = models.BooleanField(default=False, verbose_name=_('is_Staff'))
    data_joined = models.DateTimeField(auto_now_add=True, verbose_name=_('Date Joined'))
