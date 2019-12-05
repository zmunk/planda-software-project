from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.contrib.auth import logout
from .forms import RegisterForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(reverse("planner:projects_listed"))
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})


def logout_view(request):
    logout(request)
