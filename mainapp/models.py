from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User


# every class you create has to inherit from models.Model

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    u_gender = models.CharField(max_length=10)
    u_dob = models.DateField()

    def __str__(self):
        return self.user.username


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    p_title = models.CharField(max_length=20)
    p_category = models.CharField(max_length=50)
    diff_level = models.CharField(max_length=10)
    no_of_contrib = models.PositiveIntegerField()
    p_status = models.CharField(max_length=100)
    p_description = models.TextField(max_length=200)
    p_privacy = models.BooleanField(default=False)
    post_date = models.DateField()

    def __str__(self):
        return self.p_title


class ProjectSkills(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    skills = models.CharField(max_length=100)

    def __str__(self):
        return self.project.p_title

