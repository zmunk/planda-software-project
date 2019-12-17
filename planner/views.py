from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView, View
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Max
from registration.models import User
from .models import Task, Category, Project
from .forms import AddUserForm, AddTaskForm, AddCategoryForm

# DEBUGGER
import logging as log

log.basicConfig(level=log.DEBUG)  # comment this to suppress debug logging
log.debug("DEBUGGING")

"""
== Landing Page
== Project List
    -- Creating Project
    -- Deleting Project
== Project Page
    -- Project View
    -- Creating Category
    -- Updating Task Positions
    -- Deleting Category
    -- Creating Task
    -- Deleting Task
    -- Updating Task
    -- Adding User
== User Profile
"""


# ====== Landing Page
class LandingPageWithLogin(LoginView):
    template_name = 'planner/landing_page.html'
    form_class = AuthenticationForm
    redirect_authenticated_user = True


# ======= Project List

# ------ Creating Project
class ProjectCreateView(CreateView):
    model = Project
    fields = ["title"]
    template_name = "planner/projects_listed.html"

    def get_success_url(self, project_id):
        # return reverse("planner:projects_listed")
        return reverse('planner:project_page', args=(project_id,))

    def get_context_data(self, **kwargs):
        # display projects that they users_list contain the current logged in user
        context = super().get_context_data(**kwargs)
        projects = self.model.objects.filter(users_list=self.request.user)

        self.project_teams = {}
        for project in projects:
            self.project_teams[project.pk] = ", ".join([user.username for user in project.users_list.all()])

        context["project_list"] = projects
        context["project_teams"] = self.project_teams

        return context  # super(ProjectCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        project_title = form.cleaned_data['title']  # getting the entered title
        user_username = self.request.user.username  # username of current logged in user
        user = User.objects.get(username=user_username)  # user object of current logged in user

        # creating a project object adn filling the fields, then saving it.
        project_obj = Project.objects.create(creator=user)
        project_obj.users_list.add(user)
        project_obj.title = project_title
        project_obj.save()

        project_id = project_obj.pk

        return redirect(self.get_success_url(project_id))


# ------ Deleting Project
class ProjectDeleteView(DeleteView):
    model = Project

    def get_success_url(self):
        return reverse("planner:projects_listed")

    def get_object(self, **kwargs):
        pk = self.kwargs.get("project_id")
        return get_object_or_404(Project, id=pk)

    def get(self, *args, **kwargs):
        return self.delete(*args, **kwargs)


# ======= Project Page

# ------ Project View
class ProjectView(View):
    template_name = "planner/project.html"

    def get(self, request, project_id):
        user = request.user
        project = Project.objects.get(pk=project_id)
        users_list = project.users_list.all()

        # redirect if user doesn't have access
        if user not in users_list:
            return redirect(reverse("planner:landing_page"))

        project_title = project.title
        creator_username = project.creator.username
        category_list = Category.objects.filter(project=project)

        context = {
            "project_id": project_id,
            "project_title": project_title,
            "creator_username": creator_username,
            "category_list": category_list,
            "users_list": users_list,
        }

        return render(request, self.template_name, context)


# ------ Creating Lists
class CategoryCreate(View):
    model = Category
    fields = ["category_name"]

    def get_success_url(self, project_id):
        return reverse('planner:project_page', args=(self.kwargs["project_id"],))

    def post(self, request, project_id):
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            category_name = cleaned_data["category_name"]
            project = Project.objects.get(pk=project_id)
            new_category = Category(category_name=category_name, project=project)
            new_category.save()
            return redirect(self.get_success_url(project_id))


# ------ Updating Task Positions
class ProjectDataUpdate(View):
    model = Project

    def get_success_url(self, project_id):
        # pk = self.kwargs.get("project_id")
        return reverse("planner:project_page", kwargs={'project_id': project_id})

    def get(self, request, project_id):
        to_list = request.GET.get('to_list', None)
        task_id = request.GET.get('task_id', None)
        task_order = request.GET.get('task_order', None)
        print("to list: " + to_list)
        print("task id: " + task_id)
        print("task order " + task_order)

        curr_task = Task.objects.get(pk=task_id)
        old_category = curr_task.category
        old_order = curr_task.order

        new_category = Category.objects.get(pk=to_list)
        new_order = task_order

        # update order of tasks in old category
        for task in Task.objects.filter(category=old_category, order__gt=old_order):
            task.order -= 1
            task.save()

        # update order of tasks in new category
        for task in Task.objects.filter(category=new_category, order__gte=new_order):
            task.order += 1
            task.save()

        curr_task.category = new_category
        curr_task.order = new_order

        curr_task.save()

        return redirect(self.get_success_url(project_id))


# ------ Deleting Category
class CategoryDeleteView(DeleteView):
    model = Category

    def get_success_url(self):
        pk = self.kwargs.get("project_id")
        # getting id of project and passing it to project page url
        return reverse("planner:project_page", kwargs={'project_id': pk})

    def get_object(self, **kwargs):
        pk = self.kwargs.get("category_id")
        return get_object_or_404(Category, id=pk)

    def get(self, *args, **kwargs):
        return self.delete(*args, **kwargs)


# ------ Creating Task
class TaskCreate(View):
    model = Task

    def get_success_url(self, project_id):
        return reverse("planner:project_page", args=(project_id,))

    def post(self, request, project_id, category_id):
        form = AddTaskForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            text = cleaned_data["text"]
            category = Category.objects.get(pk=category_id)
            results = Task.objects.filter(category=category).aggregate(Max('order'))
            current_order = results['order__max']
            if current_order is not None:
                new_order = current_order + 1
            else:
                new_order = 0
            curr_user = request.user
            new_task = Task(text=text, category=category, author=curr_user, order=new_order)
            new_task.save()
            return redirect(self.get_success_url(project_id))


# ------ Deleting Task
class TaskDelete(DeleteView):
    model = Task

    def get_success_url(self):
        return reverse('planner:project_page', args=(self.kwargs["project_id"],))

    def get_object(self, **kwargs):
        pk = self.kwargs.get("task_id")
        return get_object_or_404(Task, id=pk)

    def get(self, *args, **kwargs):
        curr_task = self.get_object()
        order = curr_task.order
        category = curr_task.category
        for task in Task.objects.filter(category=category, order__gt=order):
            task.order -= 1
            task.save()

        return self.delete(*args, **kwargs)


# ------ Updating Task
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


# ------- Adding User
class AddUserToProject(View):
    model = Project

    def get_success_url(self, project_id):
        return reverse("planner:project_page", args=(project_id,))

    def post(self, request, project_id):
        form = AddUserForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            new_username = cleaned_data["new_user"]
            new_user = User.objects.filter(username=new_username)
            if not new_user.exists():
                messages.info(request, "User does not exist")
                return redirect(self.get_success_url(project_id))

            new_user = new_user[0]
            project = Project.objects.get(pk=project_id)

            if new_user in project.users_list.all():
                messages.info(request, "That user is already on the team")
                return redirect(self.get_success_url(project_id))

            project.users_list.add(new_user)
            project.save()
            projects = Project.objects.all()
            messages.success(request, "User was successfully added")
            return redirect(self.get_success_url(project_id), {'projects': projects})
        return redirect(self.get_success_url(project_id))


# ======= User Profile
class UserProfile(View):
    template_name = "planner/profile_page.html"

    def get(self, request, username):
        # Note: logged in user is request.user
        user = User.objects.get(username=username)
        if request.user.is_authenticated:
            context = self.get_context_data(user, request.user)
        else:
            context = self.get_context_data(user)
        return render(request, self.template_name, context)

    def get_context_data(self, user, logged_in_user=None):
        projects = Project.objects.filter(users_list__in=[user, ], private=False)

        colleagues = set()
        for project in projects:
            for colleague in project.users_list.all():
                if colleague != user:
                    colleagues.add(colleague)
        number_of_colleagues = len(colleagues)

        number_of_projects = len(projects.filter())
        first_four_projects = projects[:4]

        stock_pictures = [
            "../static/planner/images/unsplash1.jpg",
            "../static/planner/images/unsplash2.jpg",
            "../static/planner/images/unsplash3.jpg",
            "../static/planner/images/unsplash4.jpg",
        ]

        proj_and_pics = zip(first_four_projects, stock_pictures)

        # boolean that signifies whether the logged in user is the same as the user in the profile
        if not logged_in_user or logged_in_user != user:
            editable = False
        else:
            editable = True

        context = {'profile_user': user,
                   'number_of_projects': number_of_projects,
                   'projects': projects,
                   'first_four_projects': first_four_projects,
                   'stock_pictures': stock_pictures,
                   'proj_and_pics': proj_and_pics,
                   'colleagues': colleagues,
                   'number_of_colleagues': number_of_colleagues,
                   'editable': editable,
                   'logged_in_user': logged_in_user}

        return context
