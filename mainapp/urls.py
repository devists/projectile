from django.conf.urls import url
from django.contrib import admin
from . import views
from mainapp.forms import LoginForm
from django.contrib.auth.decorators import user_passes_test


login_forbidden = user_passes_test(lambda u: u.is_anonymous(), '/')

urlpatterns = [
    url(r'^register/$',  login_forbidden(views.user_register), name='register'),
    url(r'^$', views.home, name='home'),
    url(r'^reset_password', views.reset_password, name='reset_password'),
    url(r'^post_project/$', views.post_project, name='post_project'),
    url(r'^prev_posts/$', views.prev_posts, name='prev_posts'),
    url(r'^project_detail/(?P<project_id>\d+)/$', views.project_detail, name='project_detail'),
    url(r'^profile_detail/(?P<profile_id>\d+)/$', views.profile_detail, name='profile_detail'),
    url(r'^profile_update/$', views.profile_update, name='profile_update'),
    url(r'^project_edit/(?P<project_id>\d+)/$', views.project_edit, name='project_edit'),
    url(r'^profile_edit/$', views.profile_edit, name='profile_edit'),
    url(r'^projects/$', views.explore_projects, name='explore_projects'),
    url(r'^profiles/$', views.explore_profiles, name='explore_profiles'),
    url(r'^apply_project/(?P<project_id>\d+)$', views.apply_project, name='apply_project'),
    url(r'^notifications/$', views.notific, name='notific'),
    url(r'^list_of_applied_projects/$', views.list_applied, name='list_applied'),
    url(r'^activate', views.activate, name='activate'),
    url(r'^change_password', views.change_password, name='change_password'),
]
