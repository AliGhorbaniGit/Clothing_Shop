from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from accounts.models import CustomUser


class Package(models.Model):
    title = models.CharField(max_length=300, verbose_name=_('title'))
    data_created = models.DateTimeField(auto_now_add=True, verbose_name=_('data created'))
    image = models.ImageField(blank=True, upload_to='media/image', verbose_name=_('image'))
    description = models.TextField(blank=True, verbose_name=_('description'))

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(CustomUser, related_name='author',on_delete=models.CASCADE,verbose_name=_("author") )
    text = models.TextField(verbose_name=_("text"))
    data_created = models.DateTimeField(auto_now_add=True,verbose_name=_("data_created"))
    data_modified = models.DateTimeField(auto_now=True,verbose_name=_("data_modified"))









