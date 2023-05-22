from django.contrib import admin
from django.urls import path
from . import  views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.Index, name='index'),
    path('brand_register/', views.brand_register, name='brand_register'),
    path('brand_login/', views.brand_login, name='brand_login'),
    path('brand_dashboard/', views.brand_dashboard, name='brand_dashboard'),
    path('product_add/',views.product_add,name='product_add'),
    path('product_delete/',views.product_delete,name='product_delete'),
    path('product_to_update/',views.product_to_update,name='product_to_update'),
    path('product_update/',views.product_update,name='product_update'),
    path('get_single_product/<slug>',views.get_single_product,name='get_single_product'),
    path('add_to_cart/',views.add_to_cart,name='add_to_cart'),
    path('cart_detials/',views.cart_detials,name='cart_detials'),
    path('checkout/',views.checkout,name='checkout'),
    path('brand_orders/',views.brand_orders,name='brand_orders'),
    path('image_recognition/',views.image_recognition,name='image_recognition'),

]
