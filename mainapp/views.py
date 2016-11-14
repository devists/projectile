import base64
import re
import smtplib

import binascii
from Crypto.Cipher import XOR
from django.contrib import messages
from django.urls import reverse

from .forms import RegistrationForm, ProfileForm, ProjectForm,UserProfileForm, LoginForm
from .forms import RegistrationForm, ProfileForm, ProjectForm, SearchForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import ProjectSkills, Project
from django.utils import timezone
import re
from django.db.models import Q
from django.contrib.auth import authenticate, login
from .models import UserProfile,ApplyProject
from notifications.signals import notify
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# encryption key for creating activation key
secret_key = "96587411335"
# sender's email address in account verification email
email_address = "jayakishan100@gmail.com"
# sender;s email password
email_password = "52701021"


# Create your views here.
def custom_save(user):
    user.is_active = False
    user.save()

    # custom save function for creating non active user checking a user is active or not :param user:


def encrypt(key, plaintext):
    cipher = XOR.new(key)
    return base64.b64encode(cipher.encrypt(plaintext))

# encrypt a string and return :param key:param plaintext: :return: unicode(encryptedtext)


def decrypt(key, ciphertext):
    cipher = XOR.new(key)
    return cipher.decrypt(base64.b64decode(ciphertext))


# decrypt a string with key and return:param key::param ciphertext::return:decrypted text


def send_verification_mail(email, activation_key, msg):
    print("send verificaion mail")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    print("Helo")
    server.login(email_address, email_password)
    print("world")
    server.sendmail(email_address, email, msg)
    server.quit()


@login_required(login_url="login/")
def home(request):
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            query_string = search_form.cleaned_data['search_item']
            domain = search_form.cleaned_data['category']

            queries = re.split(',| ',query_string)
            #return render(request, "search_result.html", {'terms': terms})
            q=Q()
            if domain == 'Student':
                for query in queries:
                    q = q | Q(username__icontains=query)
                results= User.objects.filter(q)
                return render(request, "search_user.html", {'results': results})

            elif domain == 'Project':
                q1=Q()
                q2=Q()

                for query in queries:
                    q1 = q1 | Q(skills__icontains=query)
                    q2 = q2 | Q(p_title__icontains=query) | Q(p_category__icontains=query)
                results = ProjectSkills.objects.filter(q1)
                results_p = Project.objects.filter(q2)
            return render(request, "search_result.html", {'results': results,'results_p':results_p})

    else:
        search_form = SearchForm()
    return render(request, "home.html", {'search_form': search_form})


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
            custom_save(user)
            profile.save()

            activation_key = encrypt(secret_key, user.email)
            # sending account verification mail
            message = "Your email address is" + user.email + "activation key is " + activation_key.decode("utf-8")
            # message = "Reset link is  Emahere"
            send_verification_mail(user.email, activation_key, message)
            return HttpResponseRedirect(reverse("activate"))

    else:

        form = RegistrationForm()
        form_pro = ProfileForm()
    return render(request, 'user_reg.html', {'form': form, 'form_pro': form_pro})


def activate(request):
    # handle for user account activation:param request::return: httpresponseredirect or rendered html

    if request.method == "POST":
        email = request.POST.get("email")
        activation_key = request.POST.get("activation-key")
        # verifying thw activation key
        try:
            decoded = decrypt(secret_key, activation_key)
            decoded = decoded.decode("utf-8")
        except binascii.Error:
            decoded = None

        if email == decoded:
            user = User.objects.get(email=email)
            if user is None:
                messages.error(request, "This email id is not valid")
                return render(request, 'activation_form.html')
            # activating the user
            else:
                user.is_active = True
                user.save()
                login(request, user)

                messages.success(request, "Your Account Has been Activated..")
                return render(request, 'Succesfull_activation.html', {})

        else:
            messages.error(request, "Wrong activation key")

    return render(request, 'activation_form.html')


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

            return HttpResponse("Project Published")


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

#
# def all_projects(request):
#     # projects = Project.objects.all()
#     projects = Project.objects.get(p_title='sdsds')
#
#     if projects:
#         return render(request,'projects.html',{'projects':projects})
#


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
    profile = UserProfile.objects.filter(user=request.user)
    if request.method == "POST":
        profile = get_object_or_404(UserProfile,user=request.user)
        u_form = UserProfileForm(request.POST, instance=profile)
        if u_form.is_valid():
            profile = u_form.save(commit=False)
            profile.user = request.user
            profile.save()
            return render(request, 'profile_detail.html', {'profile': profile})

    else:
        if profile:
            profile = get_object_or_404(UserProfile,user=request.user)
            u_form = UserProfileForm(instance=profile)
            return render(request, 'profile_edit.html', {'u_form': u_form, 'profile': profile})
        else:
            return HttpResponseRedirect(reverse('profile_update'))


def explore_projects(request):
    projects = Project.objects.all()
    # projects = Project.objects.get(p_title='sdsds')

    paginator = Paginator(projects, 5) # Show 5 contacts per page

    page = request.GET.get('page')
    try:
        project_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        project_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        project_list = paginator.page(paginator.num_pages)

    return render(request, "projects.html", {'project_list': project_list})


def explore_profiles(request):
    profiles = UserProfile.objects.all()

    paginator = Paginator(profiles, 2) # Show 5 contacts per page

    page = request.GET.get('page')
    try:
        profile_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        profile_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        profile_list = paginator.page(paginator.num_pages)

    return render(request, "profiles.html", {'profile_list': profile_list})


def apply_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        apply=ApplyProject()
        apply.project = project
        apply.user = request.user
        apply.apply_date = timezone.now()
        apply.cover_letter = request.POST.get('cover')
        apply.save()
        desc = request.POST.get('cover')
        notify.send(request.user, recipient=project.user, verb='applied', target=project, description=desc)

        return redirect('home')


def notific(request):
    notice = request.user.notifications.all()
    return render(request, 'notification.html', {'notice': notice})


def list_applied(request):
    user = request.user
    ct_supported = ContentType.objects.get_for_model(user)
    lists = Notification.objects.filter(actor_content_type=ct_supported)
    return render(request, 'applied_list.html', {'lists': lists})




