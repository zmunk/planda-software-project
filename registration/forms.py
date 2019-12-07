from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    # email = forms.EmailField()
    class Meta:
        model = User
        fields = ["username", 'email', "password1", "password2"]

    # def clean_username(self, username):
    #     if User.objects.filter(username=username).exists():
    #         raise forms.ValidationError("Username is not unique")
    #
    # def clean_email(self, email):
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError("Email is not unique")


class LoginForm(forms.ModelForm):
    """Simple login form"""
    class Meta:
        model = User
        fields = ('username', 'password')



