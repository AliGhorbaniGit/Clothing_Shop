from django import forms

from .models import ContactUs


class ContactFormBySession(forms.Form):
    user_txt = forms.CharField(max_length=1000, help_text='please share us your taught', )
    admin_txt = forms.CharField(max_length=1000, required=False, )
    #
    # widgets = {admin_txt: forms.HiddenInput(), }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ('user_text',)


class ContactUpdateForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['admin_text', 'is_new', ]
