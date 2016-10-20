from django.db import models


from django.db import models


# every class you create has to inherit from models.Model
class User(models.Model):
    u_fname = models.CharField(max_length=50)
    u_lname = models.CharField(max_length=50)
    u_name = models.CharField(max_length=100)
    u_password = models.CharField(max_length=50)
    u_email = models.CharField(max_length=500)
    u_gender = models.CharField(max_length=10)
    u_dob = models.DateField(max_length=20)
    u_github = models.CharField(max_length=500)
    u_linkedin = models.CharField(max_length=500)
    u_contact_no = models.CharField(max_length=50)
    u_prof_title = models.CharField(max_length=500)
    u_mentor = models.BooleanField(default=False)
    u_location = models.CharField(max_length=1000)
    u_bio = models.CharField(max_length=5000)
    u_current_qualification = models.CharField(max_length=500, null=True)
    u_current_degree = models.CharField(max_length=500)
    u_current_college = models.CharField(max_length=1000)
    u_education_start_year = models.DateField(max_length=20)
    u_education_end_year = models.DateField(max_length=20)

    def __str__(self):
        return self.user_name


class Project(models.Model):
    user = models.ForeignKey('User', related_name='user_project')
    p_title = models.CharField(max_length=500)
    p_category = models.CharField(max_length=250)
    p_level = models.CharField(max_length=100)
    p_users_needed = models.IntegerField()
    p_status = models.CharField(max_length=200)
    p_description = models.CharField(max_length=5000)
    p_privacy = models.BooleanField(default=False)
    p_post_date = models.DateField(max_length=20)
    is_favorite = models.BooleanField(default=False)
    mentor = models.ForeignKey('User', related_name='mentor_project')

    def __str__(self):
        return self.p_title
