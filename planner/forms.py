from django import forms
from .models import Task, Project


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["text", "author"]

# testing
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title"]

