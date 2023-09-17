from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationFrom
from .models import CustomUser
from contactus.models import ContactUs


class ContactInline(admin.TabularInline):
    model = ContactUs
    fields = ['user_text', 'admin_text']


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationFrom
    From = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'password', 'is_staff']
    inlines = [ContactInline, ]


admin.site.register(CustomUser, CustomUserAdmin)
