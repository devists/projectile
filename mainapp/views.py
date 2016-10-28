from django.contrib import messages
from .forms import RegistrationForm, ProfileForm
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
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
            return HttpResponse("Successfull")
        else:
            messages.error(request, "Error")

    else:

        form = RegistrationForm()
        form_pro = ProfileForm()
    return render(request, 'mainapp/user_reg.html', {'form': form, 'form_pro': form_pro})

"""
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        passwd = request.POST.get("password")
        user = authenticate(username=username, password=passwd)
        if user is not None:
            HttpResponse("Login Successfull")
        else:
            messages.error(request, "username and password did not match")
            return render(request, "mainapp/tempo.html")

    # for a GET request
    else:
        return render(request, "mainapp/tempo.html")"""
