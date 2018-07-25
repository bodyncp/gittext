#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/6 14:40
# @Author  : NCP
# @File    : urls.py
# @Software: PyCharm

"""URLconfig URL Configuration

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
from django.conf.urls import url,include
from django.urls import path,re_path
from book_sys.views import *

urlpatterns = [
    url(r'del_book/', del_book),
    url(r'del_publish/', del_publish),
    url(r'del_author/', del_author),
    url(r'add_book/', add_book),
    url(r'add_publish/', add_publish),
    url(r'add_author/', add_author)
]