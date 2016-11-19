import base64
import smtplib

import binascii
from Crypto.Cipher import XOR
from django.contrib import messages
from django.urls import reverse
from random import randint

from .forms import RegistrationForm, ProfileForm, ProjectForm,UserProfileForm, LoginForm
from .forms import RegistrationForm, ProfileForm, ProjectForm, SearchForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Project
from django.utils import timezone
import re
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile,ApplyProject
from notifications.signals import notify
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itertools import chain


# encryption key for creating activation key
secret_key = "965874113"
# sender's email address in account verification email
email_address = "projectilehelp@gmail.com"
# sender;s email password
email_password = "projectile@help"


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
    #print("send verificaion mail")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    #print("Helo")
    server.login(email_address, email_password)
    #print("world")
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
                profile_list= User.objects.filter(q)
                return render(request, "profiles.html", {'profile_list': profile_list})

            elif domain == 'Project':
                q2=Q()

                for query in queries:
                    q2 = q2 | Q(p_title__icontains=query) | Q(p_category__icontains=query) | Q(skills__icontains=query)
                # results = ProjectSkills.objects.filter(q1)
                project_list = Project.objects.filter(q2)
            return render(request, "projects.html", {'project_list': project_list})

    else:
        search_form = SearchForm()
        user = request.user
        projects = user.project_set.all()
        aprojects = Notification.objects.filter(actor_object_id=user.id,
                                                 actor_content_type=ContentType.objects.get_for_model(user))
        if float(len(aprojects)):
            projvsapll = len(projects) / float(len(aprojects))
        else:
            projvsapll =0;
    return render(request, "home.html", {'search_form': search_form,
                                         'projects': projects, 'aprojects': aprojects, 'projvsapll':projvsapll})


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
            #activation_key =
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
                return render(request, 'successfull_activation.html', {})

        else:
            messages.error(request, "Wrong activation key")

    return render(request, 'activation_form.html')


def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = randint(10000000,99999999)

        message = "Your new password is " + str(new_password)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if user is not None:
            user.set_password(new_password)
            user.save()
            send_verification_mail(email, new_password, message)
            return HttpResponseRedirect(reverse("login"))
        else:
            messages.error(request, 'Sorry no user exist with this email address')
            return render(request, "reset_password.html")

    else:
        return render(request, "reset_password.html")


@login_required(login_url="login/")
def change_password(request):
    user = request.user
    if request.method == 'POST':
        username = user.username
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        new_password_again = request.POST.get("new_password_again")
        user = authenticate(username=username, password=old_password)
        if user is not None:
            if new_password == new_password_again:
                user.set_password(new_password)
                user.save()
                login(request,user)
                return HttpResponseRedirect(reverse("home"))
            else:
                messages.error(request, "both passwords you entered did not match")
                return render(request, 'change_password.html', {'user': user})
        else:
            messages.error(request, "sorry the password you entered is not correct")
            return render(request, 'change_password.html', {'user': user})
    else:
        return render(request, 'change_password.html', {'user': user})


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
           # project.p_title = form.cleaned_data['p_title']
            project = p_form.save(commit=False)
            project.user = request.user
            project.post_date = timezone.now()
            project.save()
            # ls = request.POST.get('skill')
            # skills = ls.split(",")

            # for skill in skills:
            #     project_s = ProjectSkills.objects.create(project=project, skills=skill)
            #     project_s.save()
            msg="Project Created Succesfully"

            return render(request, 'responseMsg.html', {'msg': msg})
        else:
            msg="Error while Creating your Project"
            return render(request, 'responseMsg.html', {'msg': msg})

    else:
        p_form = ProjectForm()

    return render(request, 'add_project.html', {'p_form': p_form})


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


def profile_detail(request, profile_id):
    profile = get_object_or_404(UserProfile, pk=profile_id)
    return render(request, 'profile_detail.html', {'profile': profile})

def app_detail(request, app_id):
    project = get_object_or_404(Notification, pk=app_id);
    return render(request, 'app_detail.html', {'project': project})


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
        profile = get_object_or_404(UserProfile, user=request.user)
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
    if request.user.is_authenticated():
        projects = Project.objects.exclude(user=request.user)
    else:
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


    return render(request, "projects.html", {'project_list': project_list,'length':len(projects)})


def explore_profiles(request):
    if request.user.is_authenticated():
        profiles = UserProfile.objects.exclude(user=request.user)
    else:
        profiles = UserProfile.objects.all()
    paginator = Paginator(profiles, 4) # Show 5 contacts per page

    page = request.GET.get('page')
    try:
        profile_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        profile_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        profile_list = paginator.page(paginator.num_pages)

    return render(request, "profiles.html", {'profile_list': profile_list,'length':len(profiles)})


def apply_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        apply = ApplyProject()
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
    projects = Notification.objects.filter(actor_object_id=user.id, actor_content_type=ContentType.objects.get_for_model(user))
    return render(request, 'applied_list.html', {'projects': projects})


def filter_search(request):
    if(request.method == "GET"):
        lists = request.GET.getlist('level')
        project_list1 = []
        project_list2 = []
        if lists:
            q = Q()
            for lis in lists:
                q = q | Q(diff_level__icontains=lis)
            project_list1 = Project.objects.filter(q)

        lists2 = request.GET.getlist('category')
        if lists2:
            q2 = Q()
            for li in lists2:
                q2 = q2 | Q(p_category__icontains=li)
            project_list2 = Project.objects.filter(q2)

        project_list = list(chain(project_list1,project_list2))

        return render(request, "projects.html", {'project_list': project_list})




        #
        # q2=Q()
        # q2 = q2 | Q(p_title__icontains=query) | Q(p_category__icontains=query) | Q(skills__icontains=query)







