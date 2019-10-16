from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import generic
from .models import Task
from .forms import TaskForm
from django.views.generic.edit import CreateView


def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task_item = form.save(commit=False)
            task_item.save()
    else:
        form = TaskForm()
    return render(request, "planner/task-form.html", {"form": form})


class IndexView(generic.ListView):
    template_name = "planner/index.html"
    context_object_name = "task_list"

    def get_queryset(self):
        return Task.objects.all()

class TaskCreate(CreateView):
    model = Task
    fields = ["text", "author"]




# class TaskCreate(CreateView):
#     model = Task
#     fields = ["text", "author"]


