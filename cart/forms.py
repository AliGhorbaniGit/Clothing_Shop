from django import forms


class AddToCartForm(forms.Form):
    """    A FORM TO ADD NEW THING TO CART   """

    QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 30)]
    """     I can write this but not professional [(1, "1"), (2, "2")]      """

    quantity = forms.TypedChoiceField(choices=QUANTITY_CHOICES, coerce=int)
    """   coerce define kind of data    """

    inplace = forms.BooleanField(required=False, widget=forms.HiddenInput)
