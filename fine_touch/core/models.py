from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


class LoggedInUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='logged_in_user')
    session_key = models.CharField(max_length=32)

    def __str__(self):
        return self.user.username


class Customer(models.Model):  # cascade means if model is deleted the relationship is also deleted
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)  # extending this model to
    # cater for users
    name = models.CharField(max_length=500, null=True)
    email = models.EmailField(null=True)

    phone_number = PhoneNumberField(null=True)
    profile_pic = models.ImageField(upload_to='media_root/profile_pic', default='cleaning-logo.png', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.name} {self.email}'


class ProductName(models.Model):
    name = models.CharField(max_length=500, null=True, db_column='Product Offered')
    slug = models.SlugField(max_length=80, unique=True)
    image = models.ImageField(upload_to='media_root', null=True, blank=True)
    description = models.TextField(db_column='Product Description')

    def get_absolute_url(self):
        return reverse("product", kwargs={
            'slug': self.slug
        })

    def __str__(self):
        return self.name


class ProductServices(models.Model):
    service_name = models.CharField(max_length=500, null=True, db_column='Services under product')
    slug = models.SlugField(max_length=200, unique=True)
    product_name = models.ForeignKey(ProductName, on_delete=models.CASCADE, related_name='product_services')
    image = models.ImageField(upload_to='media_root', null=True, blank=True)
    description = models.TextField(db_column='Service Description')

    class Meta:
        verbose_name_plural = 'Product Services'

    def get_absolute_url(self):
        return reverse("order", kwargs={
            'slug': self.slug
        })

    def __str__(self):
        return self.service_name


class Order(models.Model):
    STATUS = (
        ('0', 'Pending'),
        ('1', 'Out for delivery'),
        ('2', 'Delivered'),
    )
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(ProductServices, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=500, null=True, choices=STATUS, default=0)
    location = models.CharField(max_length=500, null=True)
    description = models.TextField(db_column='Order Description')

    def __str__(self):
        return self.product.service_name
