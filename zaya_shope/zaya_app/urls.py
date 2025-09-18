"""
URL configuration for zaya_shope project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from zaya_app import views

urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('get_productdetails/<int:id>/',views.get_productdetails,name='get_productdetails'),
    path('get_category',views.get_category,name='get_category'),
    path('product_details/<int:id>/',views.product_details,name='product_details'),
    path('shop/',views.shop,name='shop'),
    path('register/',views.register,name='register'),
    path('login/',views.user_login,name='login'),
    path('cart/',views.cart,name='cart'),
    path('checkout/', views.checkout, name="checkout"),
    path('order_success/',views.order_success,name="order_success"),
    path('addto_cart/<int:id>/',views.addto_cart,name="addto_cart"),
    path('remove_cart/<int:id>/',views.remove_cart,name="remove_cart"),
    path('update_qnty/<int:id>/',views.update_qnty,name="update_qnty"),
    path('logout_user/',views.logout_user,name='logout'),
    
   
]
