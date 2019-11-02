from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.urls import reverse_lazy, reverse
from django.views import generic
from .models import Task, Category, Project
from .forms import TaskForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.template import RequestContext

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import logging as log
log.basicConfig(level=log.DEBUG)
log.debug("DEBUGGING")


# ----------- Project
class ProjectCreate(CreateView):
    model = Project
    fields = ["title"]
    success_url = reverse_lazy("planner-namespace:projects_listed")

    # overriding form_valid method in createView to auto populate fields
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ProjectCreate, self).form_valid(form)


class ProjectView(generic.ListView):
    template_name = "planner/project.html"
    context_object_name = "category_list"

    def get_queryset(self):
        # gives category_list to project html page
        pk = self.kwargs.get("pk")
        return Category.objects.filter(project__pk=pk)

    def project_id(self):
        # allows html to access project_id through: {{ view.project_id }}
        pk = self.kwargs.get("pk")
        return pk

    def categories(self):
        project_name = self.kwargs.get("project_name")
        return Category.objects.filter(project__title=project_name)


# @method_decorator(login_required, name='dispatch') // Do not remove this line!
class ProjectsListed(generic.ListView):
    template_name = "planner/projects_listed.html"
    context_object_name = "project_list"

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)


# ----------- Category
class CategoryCreate(CreateView):
    model = Category
    fields = ["category_name"]

    def get_success_url(self):
        return reverse('planner-namespace:temp_project_page', args=(self.kwargs["pk"],))

    def get_project(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Project, id=pk)

    # overriding form_valid method in createView to auto populate fields
    def form_valid(self, form):
        form.instance.project = self.get_project()
        return super(CategoryCreate, self).form_valid(form)


# ----------- Task
class TaskCreate(CreateView):
    model = Task
    fields = ["text"] ############
    success_url = reverse_lazy("planner-namespace:project_page")

    def get_object(self, **kwargs):
        log.debug("entering taskcreate's method")
        id = self.kwargs.get("pk")
        log.debug(id)
        return get_object_or_404(Category, id=id)

    def form_valid(self, form):
        log.debug("form_valid called")
        current_category = self.get_object()
        form.instance.category = current_category
        return super(TaskCreate, self).form_valid(form)


class TaskDelete(DeleteView):
    template_name = "planner/remove-task.html"
    model = Task
    success_url = reverse_lazy("planner-namespace:project_page")

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Task, id=pk)


class DetailView(generic.DetailView):
    model = Task
    template_name = "planner/detail.html"


class TaskUpdate(UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("planner-namespace:project_page")


# ----------- Project
class DashboardView(generic.ListView):
    template_name = "dashboard/index.html"

    def get_queryset(self):
        return HttpResponse("")


