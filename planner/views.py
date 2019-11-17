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
from django.contrib.auth.models import User
# log.basicConfig(level=log.DEBUG) # comment this to suppress debug logging
log.debug("DEBUGGING")
####

class ProjectCreateView(CreateView):
    model = Project
    fields = ["title"]
    template_name = "planner/projects_listed.html"

    def get_success_url(self):
        return reverse("planner:projects_listed")

    def get_context_data(self, **kwargs):        
        #display projects that they users_list contain the current logged in user
        kwargs["project_list"] = self.model.objects.filter(users_list=self.request.user)
        return super(ProjectCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.


        project_title = form.cleaned_data['title'] #getting the entered title
        user_username = self.request.user.username #username of current logged in user
        user = User.objects.get(username= user_username) #user object of current logged in user
        
        #creating a project object adn filling the fields, then saving it. 
        project_obj = Project.objects.create(user = user)
        project_obj.users_list.add(user)
        project_obj.title = project_title
        project_obj.save()

        return redirect(self.get_success_url())


class ProjectDeleteView(DeleteView):
    model = Project

    def get_success_url(self):
        return reverse("planner:projects_listed")

    def get_object(self, **kwargs):
        pk = self.kwargs.get("project_id")
        return get_object_or_404(Project, id=pk)

    def get(self, *args, **kwargs):
        return self.delete(*args, **kwargs)


# Project page
class ProjectWithCategoryCreate(CreateView):
    model = Category
    fields = ["category_name"]
    template_name = "planner/project.html"

    def get_success_url(self):
        return reverse('planner:project_page', args=(self.kwargs["project_id"],))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("project_id")
        context["category_list"] = Category.objects.filter(project__pk=pk)
        return context

    def project_id(self):
        # allows html to access project_id through: {{ view.project_id }}
        pk = self.kwargs.get("project_id")
        return pk

    def get_project(self):
        pk = self.kwargs.get("project_id")
        return get_object_or_404(Project, id=pk)

    # overriding form_valid method in createView to auto populate fields
    def form_valid(self, form):
        form.instance.project = self.get_project()
        return super(ProjectWithCategoryCreate, self).form_valid(form)

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
