from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    # email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
        # note: can add email to fields if necessary


class LoginForm(forms.ModelForm):
    """Simple login form"""
    class Meta:
        model = User
        fields = ('username', 'password')



