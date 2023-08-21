from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Package, Comment


class PackageAdmin(admin.ModelAdmin):
    list_display = ['title', 'price']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'text']


admin.site.register(Package, PackageAdmin)
admin.site.register(Comment, CommentAdmin)
