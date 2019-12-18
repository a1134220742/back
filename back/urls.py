"""back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from back.settings import *
from app import views
from django.conf.urls import url
from django.conf.urls import include
from rest_framework import routers


urlpatterns = [
    url('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^get_papers_info/', views.paperInfo),
    url(r'^get_papers/', views.paperGet),
    url(r'^get_paper_by_id/', views.paperGetID),
    url(r'^get_favorites/', views.get_favorites),
    url(r'^get_user/', views.get_user_by_name),
    url(r'^get_follows/', views.get_follows),
    url(r'^get_chat_list/', views.get_chat_list),
    url(r'^post_message/', views.post_message),
]
