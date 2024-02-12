from django import forms


class AddToCartForm(forms.Form):
    """    A FORM TO ADD NEW PRODUCT TO CART   """

    QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 10)]

    quantity = forms.TypedChoiceField(choices=QUANTITY_CHOICES, coerce=int)
    color = forms.CharField()
    size = forms.CharField()

    inplace = forms.BooleanField(required=False, widget=forms.HiddenInput)
