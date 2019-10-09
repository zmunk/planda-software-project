from django.shortcuts import render
from django.views import generic
from .models import Task
from django.views.generic.edit import CreateView

class IndexView(generic.ListView):
    template_name = "planner/index.html"
    context_object_name = "task_list"

    def get_queryset(self):
        return Task.objects.all()

class TaskCreate(CreateView):
    model = Task
    fields = ["text", "author"]
