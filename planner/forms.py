from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    text = forms.CharField(label="Add a task", max_length=1000)
    author = forms.CharField(label="Author", max_length=100)

    # text = models.CharField(max_length=1000)
    # author = models.CharField(max_length=100)
    # password = forms.CharField(widget=forms.PasswordInput)

    # class Meta:
    #     model = Task
    #     fields = ["text", "author"]