from django import forms

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


class CustomUserCreationFrom(UserCreationForm):
    """ this is a custom form for user sign up """

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields
        widgets = {'password': forms.PasswordInput(), }


class CustomUserChangeForm(UserChangeForm):
    """ this is a custom created user form """

    class Meta:
        model = get_user_model()
        fields = UserChangeForm.Meta.fields
        widgets = {'password': forms.PasswordInput(), }


class UserInformationChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'number', 'image')
