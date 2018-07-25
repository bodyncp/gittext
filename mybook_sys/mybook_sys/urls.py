"""mybook_sys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path,re_path
from django.conf.urls import url,include
from book_sys import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('^login/$', views.login),
    re_path('^index/$', views.index),
    re_path('reg.*/', views.register),
    re_path('logout/', views.login_out),
    re_path('edit/', views.edit_book),
    re_path('edit_book_in/', views.edit_book_in),
    re_path('edit_publish/', views.edit_publish),
    re_path('edit_publish_in/', views.edit_publish_in),
    re_path('edit_author/', views.edit_author),
    re_path('edit_author_in/', views.edit_author_in),
    re_path('del_publish_list/', views.del_publish_list),
    re_path('del_author_list/', views.del_author_list),
    url('del/', include('book_sys.urls')),
    url('add/', include('book_sys.urls'))
]
