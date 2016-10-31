from django.conf.urls import url
from django.contrib import admin
from . import views
from mainapp.forms import LoginForm

urlpatterns = [
    url(r'^register/$', views.user_register, name='register'),
    url(r'^$', views.home, name='home'),
    url(r'^post_project/$', views.post_project, name='post_project'),
    url(r'^prev_posts/$', views.prev_posts, name='prev_posts'),
    url(r'^project_detail/(?P<project_id>\d+)/$', views.project_detail, name='project_detail'),
]
