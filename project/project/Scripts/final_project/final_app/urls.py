"""
URL configuration for final_project project.

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
from .import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',v.home),
    path('register',v.register_view),
    path('login',v.login_view),
    path('logout',v.logout_view),
    path('product',v.product_view),
    path('addtocart/<int:pid>',v.add_to_cart,name="addtocart"),
    path('clist',v.cartlist_view),
    path('remove/<int:pro>',v.remove_view),
    path('product_search',v.prod_search_view),
    path('product/<str:category_name>/',v.category_page,name='category_page'),
    path('sidebar',v.sidebar),
    path('filter/<int:pid>',v.filter_cate),
    path('update_cart/<int:item_id>/<str:action>/',v.update_cart, name='update_cart'),
    path('success',v.success_view),
]
