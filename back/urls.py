"""back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from app import views
from django.conf.urls import url
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login', views.login),
    path('api/sendSms', views.message),
    path('api/register', views.register),
    path('api/verify', views.verify),
    url(r'^get_experts_by_author_and_id/',views.get_experts_by_author_and_id),
    url(r'^get_experts_by_author/',views.get_experts_by_author),
    url(r'^get_experts_by_author_and_unit/',views.get_experts_by_author_and_unit),
    url(r'^api/go_follow/',views.go_follow),
    url(r'^api/go_disfollow/',views.go_disfollow),
]


