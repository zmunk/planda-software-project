from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.urls import reverse_lazy, reverse
from django.views import generic
from .models import Task, Category, Project
from .forms import TaskForm, ProjectForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.template import RequestContext

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

#### DEBUGGER
import logging as log
# log.basicConfig(level=log.DEBUG) # comment this to suppress debug logging
log.debug("DEBUGGING")
####


# --------- Testing
def project_list_view(request):
    template = "planner/projects_listed.html"
    curr_user = request.user
    form = ProjectForm(request.POST or None)
    form.instance.user = curr_user
    if request.method == "POST":
        text = request.POST.get("title")
        if not Project.objects.filter(title=text).exists():
            Project.objects.create(title=text, user=curr_user)

    project_list = Project.objects.filter(user=curr_user)
    return render(request, template, {'project_list': project_list})


# ----------- Project
class ProjectCreate(CreateView):
    model = Project
    fields = ["title"]
    success_url = reverse_lazy("planner:projects_listed")

    # overriding form_valid method in createView to auto populate fields
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.instance.user = self.request.user
        return super(ProjectCreate, self).form_valid(form)


class ProjectView(generic.ListView):
    template_name = "planner/project.html"
    context_object_name = "category_list"

    def get_queryset(self):
        # gives category_list to project html page
        pk = self.kwargs.get("project_id")
        return Category.objects.filter(project__pk=pk)

    def project_id(self):
        # allows html to access project_id through: {{ view.project_id }}
        pk = self.kwargs.get("project_id")
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
        return reverse('planner:project_page', args=(self.kwargs["project_id"],))

    def project_id(self):
        pk = self.kwargs.get("project_id")
        return pk

    def get_project(self):
        pk = self.project_id()
        return get_object_or_404(Project, id=pk)

    # overriding form_valid method in createView to auto populate fields
    def form_valid(self, form):
        form.instance.project = self.get_project()
        return super(CategoryCreate, self).form_valid(form)


# ----------- Task
class TaskCreate(CreateView):
    model = Task
    fields = ["text"]

    def get_success_url(self):
        return reverse('planner:project_page', args=(self.kwargs["project_id"],))

    def project_id(self):
        pk = self.kwargs.get("project_id")
        return pk

    def get_category(self):
        # get current category
        pk = self.kwargs.get("category_id")
        return get_object_or_404(Category, id=pk)

    def form_valid(self, form):
        log.debug("form_valid called")
        current_category = self.get_category()
        form.instance.category = current_category  # fill category
        form.instance.author = self.request.user  # fill user
        return super(TaskCreate, self).form_valid(form)


class TaskDelete(DeleteView):
    template_name = "planner/remove-task.html"
    model = Task

    def get_success_url(self):
        # project_id  = something
        return reverse('planner:project_page', args=(self.kwargs["project_id"],))

    def get_project_id(self, **kwargs):
        pk = self.kwargs.get("project_id")
        return pk

    def get_object(self, **kwargs):
        pk = self.kwargs.get("task_id")
        return get_object_or_404(Task, id=pk)

    def category_id(self):
        # allows html to access project_id through: {{ view.project_id }}
        pk = self.kwargs.get("category_id")
        return get_object_or_404(Category, id=pk)


class DetailView(generic.DetailView):
    model = Task
    template_name = "planner/detail.html"

    def project_id(self):
        pk = self.kwargs.get("project_id")
        return pk


class TaskUpdate(UpdateView):
    model = Task
    fields = ["text"]

    def get_success_url(self):
        return reverse('planner:project_page', args=(self.kwargs["project_id"],))

    def project_id(self):
        pk = self.kwargs.get("project_id")
        return pk

    def get_object(self, queryset=None):
        pk = self.kwargs.get("task_id")
        return get_object_or_404(Task, id=pk)


# ----------- Project
class DashboardView(generic.ListView):
    template_name = "dashboard/index.html"

    def get_queryset(self):
        return HttpResponse("")
