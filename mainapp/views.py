from django.contrib import messages
from .forms import RegistrationForm, ProfileForm, ProjectForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import ProjectSkills,Project
from django.utils import timezone

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


def post_project(request):
    if request.method == "POST":

        user = request.user

        p_form = ProjectForm(request.POST)
        if p_form.is_valid():

            project = p_form.save(commit=False)
            project.user = user
            project.post_date = timezone.now()
            project.save()
            ls = request.POST.get('skill')
            skills = ls.split(",")

            for skill in skills:
                project_s = ProjectSkills.objects.create(project=project, skills=skill)
                project_s.save()

            return HttpResponse("Project Published")

    else:
        p_form = ProjectForm()

    return render(request, 'tempo.html', {'p_form': p_form})

def prev_posts(request):

    user=request.user

    projects = user.project_set.all()

    if projects:

        return render(request, 'prev_projects.html', {'projects':projects})

    else:
        return HttpResponse("You havent posted any projects yet")


def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'project_detail.html', {'project': project})












