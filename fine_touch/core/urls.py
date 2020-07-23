from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),

    path('admin_page/', views.admin_dash, name='admin_dash'),
    path('add_product_name/', views.create_product, name='create_product'),
    path('update_product_name/<slug>', views.update_product, name='update_product'),
    path('delete_product_name/<slug>', views.delete_product, name='delete_product'),

    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('order/<slug>', views.order, name='order'),
    path('services/', views.services, name='services'),
    path('product/<slug>', views.product, name='product'),
]