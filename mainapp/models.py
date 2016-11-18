from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField



# every class you create has to inherit from models.Model

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    u_gender = models.CharField(max_length=10)
    u_dob = models.DateField()

    def __str__(self):
        return self.user.username


class Project(models.Model):
    OPTIONS = (
                ("python", "Python"),
                ("django", "Django"),
                ("java", "Java"),
                )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    p_title = models.CharField(max_length=200)
    p_category = models.CharField(max_length=500)
    diff_level = models.CharField(max_length=1000)
    no_of_contrib = models.PositiveIntegerField()
    p_status = models.CharField(max_length=100)
    p_location = models.CharField(max_length=20, null=True)
    p_description = models.TextField(max_length=200)
    p_privacy = models.BooleanField(default=False)
    skills = MultiSelectField(choices=OPTIONS, max_length=6000)
    #skills = ArrayField(models.CharField(max_length=200), blank=True)
    post_date = models.DateField()

    def __str__(self):
        return self.p_title


class UserProfile(models.Model):
    OPTIONS = (
                ("Python", "Python"),
                ("Django", "Django"),
                ("Java", "Java"),
                )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    u_github = models.URLField(max_length=500)
    u_linkedin = models.URLField(max_length=500)
    u_contact_no = models.CharField(max_length=50, blank=True, default='')
    u_prof_title = models.CharField(max_length=500)
    u_location = models.CharField(max_length=1000)
    u_bio = models.TextField(default='', blank=True,max_length=2000)
    u_current_qualification = models.CharField(max_length=500)
    u_current_degree = models.CharField(max_length=500)
    u_current_college = models.CharField(max_length=1000)
    u_education_start_year = models.CharField(max_length=4)
    u_education_end_year = models.CharField(max_length=4)
    skills = MultiSelectField(choices=OPTIONS, max_length=6000)

    def __str__(self):
        return self.user.username


class ApplyProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    approval = models.BooleanField(default=False)
    apply_date = models.DateField()
    cover_letter = models.TextField()

    def __str__(self):
        return self.user.username+" applied to "+self.project.p_title


