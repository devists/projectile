from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Project, ProjectSkills, Student, UserProfile
import datetime


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'First_Name'}))
    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Last_Name'}))
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'UserName'}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Re-Enter Password'}))
    email = forms.EmailField(label='', required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            "Email Already Exists")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            "Username has been Taken, Try other one")

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data and self.cleaned_data['password1'] != \
                self.cleaned_data['password2']:
            raise forms.ValidationError("The password does not match ")
        return self.cleaned_data


class DateInput(forms.DateInput):
    input_type = 'date'


class ProfileForm(forms.ModelForm):
    CHOICES = [('M', 'Male'),
               ('F', 'Female')]

    u_gender = forms.ChoiceField(label='Gender', choices=CHOICES, widget=forms.RadioSelect())
    u_dob = forms.CharField(label='Date Of Birth', widget=DateInput())

    class Meta:
        model = Student
        fields = ['u_gender', 'u_dob']


class ProjectForm(forms.ModelForm):
    CHOICES = [('B', 'Beginner'),
               ('I', 'Intermediate'),
               ('A', 'Advanced')]

    p_title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'name': 'title'}))
    p_category = forms.CharField(label='Category', widget=forms.TextInput(attrs={'name': 'category'}))
    diff_level = forms.ChoiceField(label='Difficulty-Level', choices=CHOICES,
                                   widget=forms.RadioSelect(attrs={'name': 'level'}))
    p_description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'name': 'description'}))
    no_of_contrib = forms.CharField(label='No. of Contributors Needed',
                                    widget=forms.TextInput(attrs={'type': 'number', 'name': 'contrib'}))
    p_status = forms.CharField(label='Project-Status', widget=forms.TextInput(attrs={'name': 'status'}))
    p_privacy = forms.BooleanField(label='Privacy',required=False, widget=forms.CheckboxInput(attrs={'name': 'privacy'}))

    class Meta:
        model = Project
        fields = ['p_title', 'p_category', 'diff_level', 'p_description', 'no_of_contrib', 'p_status', 'p_privacy']


class UserProfileForm(forms.ModelForm):
    #username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'name': 'username'}))
    YEAR_CHOICES = []
    for r in range(1980, (datetime.datetime.now().year + 1)):
        YEAR_CHOICES.append((r, r))

    u_github = forms.CharField(label='Github', widget=forms.TextInput(attrs={'name': 'github'}),required=True)
    u_linkedin = forms.CharField(label='Linkedin', widget=forms.TextInput(attrs={'name': 'linkedin'}),required=True)
    u_contact_no = forms.CharField(label='Contact_no',
                                   widget=forms.NumberInput(attrs={'name': 'contact_no'}), required=True)
    u_prof_title = forms.CharField(label='Professional_title',
                                   widget=forms.TextInput(attrs={'name': 'prof_title'}), required=True)

    u_location = forms.CharField(label='Location', widget=forms.TextInput(attrs={'name': 'location'}), required=True)
    u_bio = forms.TextInput()
    u_current_qualification = forms.CharField(label='Current_qualification',
                                              widget=forms.TextInput(attrs={'name': 'current_qualification'}),
                                              required=True)

    u_current_degree = forms.CharField(label='Current_degree',
                                       widget=forms.TextInput(attrs={'name': 'current_degree'}), required=True)

    u_current_college = forms.CharField(label='Current_college',
                                        widget=forms.TextInput(attrs={'name': 'current_college'}), required=True)

    u_education_start_year = forms.ChoiceField(label='Education_start_year', choices=YEAR_CHOICES,
                                               widget=forms.TextInput(attrs={'name': 'education_start_year'}),
                                               required=True)
    u_education_end_year = forms.ChoiceField(label='Education_end_year', choices=YEAR_CHOICES,
                                             widget=forms.TextInput(attrs={'name': 'education_end_year'}), required=True)

    class Meta:
        model = UserProfile
        fields = ['u_github', 'u_linkedin', 'u_contact_no', 'u_prof_title', 'u_location', 'u_bio',
                  'u_current_qualification',  'u_current_degree', 'u_current_college', 'u_education_start_year',
                  'u_education_end_year']

class SearchForm(forms.Form):

    CATEGORIES = (
    ('Project', 'Project'),
    ('Student', 'Users'),

)
    search_item = forms.CharField(label='Keyword Search', max_length=30,widget=forms.TextInput(attrs={'name': 'title'}))
    category = forms.ChoiceField(choices=CATEGORIES, required=True)
