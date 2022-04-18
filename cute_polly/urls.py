from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('l-cab/', admin.site.urls),
    path('', include('mailer.urls')),
    path('users/', include('accounts.urls')),
    path('clients/', include('clients.urls'))
]
