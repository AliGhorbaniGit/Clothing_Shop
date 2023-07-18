from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from django.db import models


class Cart(models.Model):
    user = models.ForeignKey(get_user_model, on_delete=models.CASCADE, verbose_name=_('user'))

