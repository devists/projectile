from django.db import models
from django.contrib.auth.models import User


# every class you create has to inherit from models.Model

class Student(models.Model):
    user = models.OneToOneField(User)
    u_gender = models.CharField(max_length=10)
    u_dob = models.DateField(max_length=20)
    u_github = models.CharField(max_length=500)
    u_linkedin = models.CharField(max_length=500)
    u_contact_no = models.CharField(max_length=50, blank=True, default='')
    u_prof_title = models.CharField(max_length=500)
    u_mentor = models.BooleanField(default=False)
    u_location = models.CharField(max_length=1000)
    u_bio = models.TextField(default='', blank=True)
    u_current_qualification = models.CharField(max_length=500, null=True)
    u_current_degree = models.CharField(max_length=500)
    u_current_college = models.CharField(max_length=1000)
    u_education_start_year = models.DateField(max_length=20)
    u_education_end_year = models.DateField(max_length=20)

    def __str__(self):
        return self.user_name


