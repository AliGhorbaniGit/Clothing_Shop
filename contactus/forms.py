from django import forms

from .models import ContactUs


class ContactForm(forms.Form):
    user_txt = forms.CharField(max_length=255, help_text=' how we can help you ', )
    admin_txt = forms.CharField(max_length=255, required=False, )
    # widgets = {admin_txt: forms.HiddenInput(), }


class UserContactForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ('user_text',)


class AdminContactForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['admin_text', 'is_new', ]
