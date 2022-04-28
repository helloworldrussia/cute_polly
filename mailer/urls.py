from django.contrib import admin
from django.urls import path, include

from mailer.views import IndexView, client_ask, add_emails, invite, inv_form

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('invite/', inv_form, name='inv_form'),
    path('email/<str:type>/<str:email>', client_ask),
    path('download/', add_emails, name='download'),
    path('invite/', invite, name='invite'),
]