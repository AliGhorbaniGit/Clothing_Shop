from django.contrib import admin

from .models import ContactUs


class ContactAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_new',
                    'user_sent_date_time', ]


admin.site.register(ContactUs, ContactAdmin)
