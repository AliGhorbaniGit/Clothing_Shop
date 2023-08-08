from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationFrom
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationFrom
    From = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'password', 'is_staff']


admin.site.register(CustomUser, CustomUserAdmin)
