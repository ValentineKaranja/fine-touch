from django.contrib import admin
from .models import *

# Register your models here.


class ProductServiceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('service_name',)}


class ProductNameAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(ProductServices, ProductServiceAdmin)
admin.site.register(Customer)
admin.site.register(ProductName, ProductNameAdmin)
admin.site.register(Order)