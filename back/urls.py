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
from django.conf.urls import url
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login),
    url(r'^sendSms/', views.message),
    url(r'^register/', views.register),
    url(r'^verify/', views.verify),
    url(r'^islogin/', views.islogin),
    url(r'^get_experts_by_author_and_id/',views.get_experts_by_author_and_id),
    url(r'^get_experts_by_author/',views.get_experts_by_author),
    url(r'^get_experts_by_author_and_unit/',views.get_experts_by_author_and_unit),
    url(r'^go_follow/',views.go_follow),
    url(r'^go_disfollow/',views.go_disfollow),
    url('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^get_papers_info/', views.paperInfo),
    url(r'^get_papers/', views.paperGet),
    url(r'^get_papers_by_year/', views.paperGetByYear),
    url(r'^get_papers_by_author/', views.paperGetByAuthor),
    url(r'^get_paper_total_by_year/', views.paperGetByYearTotal),
    url(r'^get_paper_total_by_author/', views.paperGetByAuthorTotal),
    url(r'^get_paper_by_id/', views.paperGetID),
    url(r'^get_favorites/', views.get_favorites),
    url(r'^get_user/', views.get_user_by_name),
    url(r'^get_follows/', views.get_follows),
    url(r'^get_chat_list/', views.get_chat_list),
    url(r'^post_message/', views.post_message),
    url(r'^go_follow_by_user_id_and_author_and_unit/',views.go_follow_by_user_id_and_author_and_unit),
    url(r'^go_disfollow_by_user_id_and_author_and_unit/',views.go_disfollow_by_user_id_and_author_and_unit),
    url(r'^get_head_url/',views.get_head_url),
    url(r'^application_for_expert/',views.application_for_expert),
    url(r'^handle_the_application/',views.handle_the_application),
    url(r'^get_iffollowed/',views.get_iffollowed),
    url(r'^newest/',views.newest),
    url(r'^admin/login/',views.admin_login),
    url(r'^admin/getData/',views.admin_getData),
]


