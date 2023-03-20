"""Shopify URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from accounts import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register',views.Register.as_view(),name='register'),
    path('login/',obtain_auth_token,name='login'),
    path('welcome',views.Welcome.as_view(),name='welcome'),
    path('edit_profile',views.EditProfile.as_view(),name='editprofile'),
    path('api/v1/',include('store.urls'))
    ] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
