from django.contrib import admin
from django.urls import path, include

from clients.views import client_sub

urlpatterns = [
    path('sub/', client_sub, name='clients_sub'),
]