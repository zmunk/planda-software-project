from django import forms
from .models import Task, Project
from django.db import models


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["text", "author"]


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title"]


class AddUserForm(forms.Form):
    new_user = forms.CharField(max_length=1000)
