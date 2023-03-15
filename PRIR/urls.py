from django.contrib import admin
from django.urls import path
from . import  views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Index, name='index'),
    path('brand_register/', views.brand_register, name='brand_register'),
    path('brand_login/', views.brand_login, name='brand_login')

]
