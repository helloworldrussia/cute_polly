from django.http import HttpResponse
from django.shortcuts import render, redirect

from mailer.models import Address


def client_sub(request):
    if request.method == "POST":
        email = request.POST['email']
        print(email)
        try:
            obj = Address.objects.get(email=email)
            obj.status = 'subscribe'
            obj.save()
        except:
            obj = Address()
            obj.email = email
            obj.status = 'subscribe'
            obj.save()
        return redirect('https://google.com')
    else:
        return render(request, 'sub.html')