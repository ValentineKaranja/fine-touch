from django import forms
from .models import Order


class OrderForm(forms.Form):
    location = forms.CharField(
        max_length=99,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Tell us your location, eg. Fitz building next to TRM"
        })
    )
    description = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "placeholder": "eg.I need general cleaning at my house. or  Cook and deliver beef stew  or  egg-avocago salad"
        })
    )
