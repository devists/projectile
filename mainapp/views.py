from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import View
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from .forms import RegistrationForm, ProfileForm
from django.contrib.auth.models import User


# Create your views here.
def initiate(request):
    return render(request,'mainapp/start.html',{})


def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST) #This will be used in POST request
        form_pro = ProfileForm(request.POST)
        if form.is_valid() and form_pro.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            profile = form_pro.save(commit=False)
            profile.user = user
            user.save()
            profile.save()
            return render(request,'mainapp/user_login.html',{})
        else:
            messages.error(request, "Error")

    else:

        form = RegistrationForm()
        form_pro = ProfileForm()
    return render(request, 'mainapp/user_reg.html', {'form': form, 'form_pro': form_pro})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request,user)
                return render(request,'mainapp/user_logout.html',{})

        else:
            return HttpResponse("You dont have an account on this, Please sign up first")
    else:
        return render(request, 'mainapp/user_login.html', {})


def user_logout(request):
    logout(request)
    if request.method == 'POST':
        return redirect(user_login)

