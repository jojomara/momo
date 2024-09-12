"""
URL configuration for grocery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin # type: ignore
from django.urls import path # type: ignore
from groceryapp import views

 # type: ignore

from django.contrib.auth import views as auth_views # type: ignore we are acssesing the views flies wic are found in our app folder(grocery_app)v;

urlpatterns = [
 path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),  # Custom login view
    path('logout/', views.user_logout, name='logout'),  # Custom logout view
    path('issue_item/<int:pk>/', views.issue_item, name='issue_item'),
    path('credit-sales/', views.CreditSaleListView.as_view(), name='credit_sale_list'),

    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('receipt/', views.receipt, name='receipt'),
    path('receipt/<int:receipt_id>/', views.receipt_detail, name='receipt_detail'),
    path('delete-receipt/<int:id>/', views.delete_receipt, name='delete_receipt'),
    path('add-credit-sale/', views.creditsale, name='creditsale'),
    path('credit-sales/', views.credit_sales_list, name='credit_sales_list'),
     path('add-stock/<int:product_id>/', views.Addstock, name='Addstock'),
    # path('product/Astock/<int:product_id>/', views.Astock, name='Astock'),
    


    # Optionally, you can use Django's built-in authentication views
    path('accounts/login/', auth_views.LoginView.as_view(template_name='groceryapp/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='groceryapp/logout.html'), name='logout'),
]