from django import forms
from django.contrib.auth.models import User
from .models import Student
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,initial='',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,initial='',
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

    """def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            "UserName has been Taken")"""
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            "Email Already Exists")

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data and self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise forms.ValidationError("The password does not match ")
        return self.cleaned_data


class DateInput(forms.DateInput):
    input_type = 'date'


class ProfileForm(forms.ModelForm):

    CHOICES = [('M', 'Male'),
         ('F', 'Female')]

    u_gender = forms.ChoiceField(label='Gender', choices=CHOICES, widget=forms.RadioSelect())
    u_dob = forms.DateField(label='Date Of Birth', widget=DateInput())

    class Meta:
        model = Student
        fields = ['u_gender', 'u_dob']



