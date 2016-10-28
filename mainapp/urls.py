from django.conf.urls import url
from django.contrib import admin
from . import views
from mainapp.forms import LoginForm

urlpatterns = [
    url(r'^register/$', views.user_register, name='register'),
    url(r'^$', views.home, name='home'),
]
