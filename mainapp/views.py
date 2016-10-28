from django.contrib import messages
from .forms import RegistrationForm, ProfileForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url="login/")
def home(request):
    return render(request, "home.html")


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
            return redirect('/login')
        else:
            messages.error(request, "Error")

    else:

        form = RegistrationForm()
        form_pro = ProfileForm()
    return render(request, 'user_reg.html', {'form': form, 'form_pro': form_pro})

