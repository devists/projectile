from django.db import models
from django.contrib.auth.models import User


# every class you create has to inherit from models.Model

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    u_gender = models.CharField(max_length=10)
    u_dob = models.DateField()

    def __str__(self):
        return self.user.username


