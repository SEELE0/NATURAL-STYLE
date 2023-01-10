from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include

from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.index),
    path('generic/',views.index),
    path('index/',include('app01.urls')),
    ]
