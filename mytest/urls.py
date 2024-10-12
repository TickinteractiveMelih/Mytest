from django.urls import path

from django.shortcuts import render

from mytest import views



urlpatterns = [
    path('', views.index, name='test'),
    path('send_message_to_all/', views.send_message_to_all, name='send_message_to_all'),
]