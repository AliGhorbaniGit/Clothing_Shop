from django.contrib import admin

from .models import Package


class AddPackageToAdmin(admin.ModelAdmin):
    pass


admin.site.register(Package,AddPackageToAdmin)

