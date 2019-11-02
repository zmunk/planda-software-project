from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.urls import reverse_lazy
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



class ProjectView(generic.ListView):
    template_name = "planner/project.html"
    context_object_name = "category_list"

    # def get_queryset(self):
    #     # project_name = self.kwargs.get("project_name")
    #     pk = self.kwargs.get("pk")
    #     log.debug(f"in project view, pk: {pk}")
    #     context = {
    #         "categories": Category.objects.filter(project__id=pk),
    #         "project_id": pk,  # TODO
    #     }################################
    #
    #     return render_to_response(self.template_name, context)
    #     # return render(request, 'Articles/greeting.html', context)
    def get_queryset(self):
        # project_name = self.kwargs.get("project_name")
        pk = self.kwargs.get("pk")

        log.debug(f"project id: {pk}")
        return Category.objects.filter(project__pk=pk)
        # return Category.objects.filter(project__title=project_name)
    #
    # def get_context_data(self, **kwargs):
    #     context = super(ProjectView, self).get_context_data(**kwargs)
    #     # context['tags'] = Tag.objects.all()
    #     pk = self.kwargs.get("pk")
    #     # q = Category.objects.filter(project__pk=pk) ############
    #     context["categories"] = Category.objects.all().filter(project__pk=pk)
    #     # log.debug("categories: " + str(q.query))
    #     context["project_id"] = pk  #######################################3
    #     return context

    def project_id(self):
        pk = self.kwargs.get("pk")
        return pk

    def categories(self):
        project_name = self.kwargs.get("project_name")
        return Category.objects.filter(project__title=project_name)

    # def get(self):
    #     context = {
    #         "categories": Category.objects.filter(project__title=project_name),
    #         "project_id": self.kwargs.get("pk")
    #     }
        # return Category.objects.filter(project__title=project_name)
        ########################################
        # return project.id
 

# @method_decorator(login_required, name='dispatch') // Do not remove this line!
class ProjectsListed(generic.ListView):
    template_name = "planner/projects_listed.html"
    context_object_name = "project_list"

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)


class DashboardView(generic.ListView):
    template_name = "dashboard/index.html"

    def get_queryset(self):
        return HttpResponse("")

# class IndexView(generic.ListView):
#     template_name = "planner/index.html"
#     # context_object_name = "task_list"
#     context_object_name = "category_list"
#
#     def get_queryset(self):
#         # return Task.objects.all()
#         return Category.objects.all()


class TaskCreate(CreateView):
    model = Task
    fields = ["text", "author", "user"]
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


class TaskUpdate(UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("planner-namespace:project_page")


class CategoryCreate(CreateView):
    model = Category
    fields = ["category_name"]
    # fields = "__all__"
    success_url = reverse_lazy("planner-namespace:project_page")

    def get_project(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Project, id=pk)

    # overriding form_valid method in createView to auto populate fields
    def form_valid(self, form):
        form.instance.project = self.get_project()
        return super(CategoryCreate, self).form_valid(form)


class ProjectCreate(CreateView):
    model = Project
    fields = ["title"]
    # fields = "__all__"
    success_url = reverse_lazy("planner-namespace:projects_listed")

    # overriding form_valid method in createView to auto populate fields
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ProjectCreate, self).form_valid(form)