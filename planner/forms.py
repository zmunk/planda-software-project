from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    text = forms.CharField(label="Add a task", max_length=1000, required=True)
    author = forms.CharField(label="Author", max_length=100, required=True)

    class Meta:
        model = Task
        fields = ["text", "author"]