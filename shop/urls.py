from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('add-to-cart/<int:product_id>/', views.cart_add, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
]