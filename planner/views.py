from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from .models import Task
from .forms import TaskForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView


class TaskDelete(DeleteView):
    model = Task
    success_url = reverse_lazy("planner-namespace:index")


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


