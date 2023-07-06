from django.contrib import admin

from .models import Package, Comment


class AddPackageToAdmin(admin.ModelAdmin):
    pass


admin.site.register(Package, AddPackageToAdmin)
admin.site.register(Comment, AddPackageToAdmin)
