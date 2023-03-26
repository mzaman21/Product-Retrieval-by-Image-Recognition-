from django.urls import path, include
from . import views


urlpatterns = [
    path('',views.userHome,name="uhome"),
    path('usignup/', views.userSignUp, name="usignup"),
    path('ulogin/', views.userLogin, name="ulogin"),
    path('usignout/', views.uSingOut, name="usignout"),

]


