from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .models import Task
from .forms import TaskForm
from django.views.generic.edit import CreateView, UpdateView


def remove_task(request, id=None):
    task = get_object_or_404(Task,id=id)
    if request.method=="POST":
        task.delete()
        messages.success(request, "Task Successfully Deleted !")
        return redirect("/")
    return render(request, "planner/remove-task.html")

class DetailView(generic.DetailView):
    model = Task
    template_name = "planner/detail.html"

class IndexView(generic.ListView):
    template_name = "planner/index.html"
    context_object_name = "task_list"

    def get_queryset(self):
        return Task.objects.all()

class TaskCreate(CreateView):
    model = Task
    fields = "__all__"

###

class TaskUpdate(UpdateView):
    model = Task
    fields = "__all__"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
###


