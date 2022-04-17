from django.http import HttpResponse
from django.shortcuts import render

from mailer.models import Address


def client_sub(request):
    if request.method == "POST":
        email = request.POST['email']
        try:
            obj = Address.objects.get(email=email)
            obj.status = 'subscribe'
            obj.save()
        except:
            obj = Address()
            obj.email = email
            obj.status = 'subscribe'
            obj.save()
        return HttpResponse(200)
    else:
        return HttpResponse(404)