"""
URL configuration for video_project project.

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
from .views import *

urlpatterns = [
    path("",index,name="index"),
    path("registration",register,name="register"),
    path("login",login,name="login"),
    path("forget",forget,name="forget"),
    path('video_details/<int:id>', video_details, name='video_details'),
    path("delete_all",delete_all,name='delete_all'),
    path('like_video/<int:id>', like_video, name='like_video'),
    path("c_password",c_password,name="c_password"),
    path('create_video', create_video, name='create_video'),
    path('search_function',search_function,name="search_function"),
    path("search",search,name="search"),
    path("logout",logout,name="logout"),
    path("profile",profile,name="profile"),
    path("edit",edit,name="edit"),
    path("category",category_list,name="category"),
    path("show_watch_letter",show_watch_letter,name="show_watch_letter"),
    path("watch_letter/<int:id>",watch_letter,name='watch_letter'),
    path('display_category/<int:id>',display_category,name='display_category'),
    path('subscriber_channle/<int:id>',subscriber_channle,name='subscriber_channle'),
    path('delete_watchlatter/<int:id>',delete_watchlatter,name='delete_watchlatter'),
    path("subscriber_Details",subscriber_Details,name="subscriber_Details"),
    path('show_all_post',show_all_post,name='show_all_post'),
    path('trending',trending,name='trending'),
    path("delete_video/<int:id>",delete_video,name='delete_video'),
    path("edit_video/<int:id>",edit_video,name='edit_video'),
    path("delete_account/<int:id>",delete_account,name='delete_account'),
        
]
