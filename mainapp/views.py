from django.contrib import messages
from .forms import RegistrationForm, ProfileForm, ProjectForm,UserProfileForm, LoginForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import ProjectSkills, Project
from django.utils import timezone
from django.contrib.auth import authenticate, login

from .models import UserProfile
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
            login(request, user)
            return redirect('profile_update')
        else:
            messages.error(request, "Error")

    else:

        form = RegistrationForm()
        form_pro = ProfileForm()
    return render(request, 'user_reg.html', {'form': form, 'form_pro': form_pro})


def profile_update(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('home')

    else:
        form = UserProfileForm()
    return render(request, 'profile_update.html', {'form': form})


def post_project(request):
    if request.method == "POST":
        p_form = ProjectForm(request.POST)
        if p_form.is_valid():

            project = p_form.save(commit=False)
            project.user = request.user
            project.post_date = timezone.now()
            project.save()
            ls = request.POST.get('skill')
            skills = ls.split(",")

            for skill in skills:
                project_s = ProjectSkills.objects.create(project=project, skills=skill)
                project_s.save()

            return HttpResponse("Succesfull")

    else:
        p_form = ProjectForm()
    return render(request, 'tempo.html', {'p_form': p_form})


def prev_posts(request):

    user = request.user

    projects = user.project_set.all()

    if projects:

        return render(request, 'prev_projects.html', {'projects': projects})

    else:
        return HttpResponse("You haven't posted any projects yet")


def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'project_detail.html', {'project': project})


def project_edit(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        e_form = ProjectForm(request.POST, instance=project)
        if e_form.is_valid():
            project = e_form.save(commit=False)
            project.save()
            return render(request, 'project_detail.html', {'project': project})

    else:
        e_form = ProjectForm(instance=project)
    return render(request, 'project_edit.html', {'e_form': e_form, 'project': project})


def profile_edit(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        u_form = UserProfileForm(request.POST, instance=profile)
        if u_form.is_valid():
            profile = u_form.save(commit=False)
            profile.user = request.user
            profile.save()
            return render(request, 'profile_detail.html', {'profile': profile})

    else:
        u_form = UserProfileForm(instance=profile)
    return render(request, 'profile_edit.html', {'u_form': u_form, 'profile': profile})











