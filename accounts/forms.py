from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


class CustomUserCreationFrom(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email')
        widgets = {'password': forms.PasswordInput()}


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password',)
        widgets = {'password': forms.PasswordInput(), }
