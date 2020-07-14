from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('order/<slug>', views.order, name='order'),
    path('services/', views.services, name='services'),
    path('product/<slug>', views.product, name='product'),
]