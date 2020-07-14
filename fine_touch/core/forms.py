from django import forms
from .models import Order


class OrderForm(forms.Form):
    location = forms.CharField(
        max_length=99,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Tell us your location"
        })
    )
    description = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "placeholder": "Describe your order specifics"
        })
    )
