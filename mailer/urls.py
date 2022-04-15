from django.contrib import admin
from django.urls import path, include

from mailer.views import IndexView, test, client_ask, add_emails, invite

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('test/', test),
    path('email/<str:type>/<str:email>', client_ask),
    path('download/', add_emails, name='download'),
    path('invite/', invite, name='invite'),
]