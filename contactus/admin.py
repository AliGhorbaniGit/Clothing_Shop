from django.contrib import admin

# from .contact import ContactUs
from .models import ContactUs


class ContactAdmin(admin.ModelAdmin):
    list_display = ['user', ]
# class ContactAdmin(admin.ModelAdmin):
#     pass


# admin.site.register(ContactUs, ContactAdmin)
admin.site.register(ContactUs, ContactAdmin)
