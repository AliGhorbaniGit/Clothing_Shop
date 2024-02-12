from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone_number', 'address', 'order_notes', ]
        widgets = {
            'order_notes': forms.Textarea(attrs={'rows': 5, 'placeholder': 'any note that u want to add'}),
        }
