from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('store/', views.store, name='store'),
    path('order/', views.order, name='order'),
    path('services/', views.services, name='services'),
    path('product/', views.product, name='product'),
]