"""
URL configuration for company_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from company.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('user_signup/', user_signup, name='user_signup'),
    path('user_login/', user_login, name='user_login'),
    path('details/', login_submit, name='details'),
    path('login/', signup_submit, name='login'),
    path('logout/', user_logout, name='logout'),
    path('edit/', edit, name='edit'),


    # separate CRUD APIs for User and Company which can be accessed by admin users only
    # create and get all users api
    path('users/', CustomUserView.as_view(), name='user'),
    # get, edit and delete user details api
    path('users/<int:user_id>', CustomUserView.as_view(), name='user'),
    # create and get all companies api
    path('company/', CompanyView.as_view(), name='company'),
    # get, edit and delete company details api
    path('company/<int:id>', CompanyView.as_view(), name='company'),

]
