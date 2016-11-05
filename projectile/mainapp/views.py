from django.shortcuts import render


# Create your views here.


def initiate(request):
    posts = 'Hello Projectile'
    return render(request, 'mainapp/tempo.html', {'posts': posts})
