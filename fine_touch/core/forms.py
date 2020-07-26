from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Order, Customer, ProductName, ProductServices


# class OrderForm(forms.Form):
#     location = forms.CharField(
#         max_length=99,
#         widget=forms.TextInput(attrs={
#             "class": "form-control",
#             "placeholder": "Tell us your location, eg. Fitz building next to TRM"
#         })
#     )
#     description = forms.CharField(widget=forms.Textarea(
#         attrs={
#             "class": "form-control",
#             "placeholder": "eg.I need general cleaning at my house. or  Cook and deliver beef stew  or  egg-avocago "
#                            "salad "
#         })
#     )

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['location', 'description']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'  # [takes in a list of fields to use]
        exclude = ['user']


class ProductNameForm(ModelForm):
    class Meta:
        model = ProductName
        fields = '__all__'
        exclude = ['slug']


class ProductServicesForm(ModelForm):
    class Meta:
        model = ProductServices
        fields = '__all__'
        exclude = ['slug', 'product_name']
