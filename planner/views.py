from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.urls import reverse
from django.views.generic.detail import SingleObjectMixin

from .models import Task, Category, Project
from django.views.generic.edit import CreateView, UpdateView, DeleteView, View
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from registration.forms import LoginForm
from .forms import AddUserForm, AddTaskForm

from django.contrib import messages

#### DEBUGGER
import logging as log
# from django.contrib.auth.models import User
from registration.models import User

log.basicConfig(level=log.DEBUG)  # comment this to suppress debug logging
log.debug("DEBUGGING")


####


class LandingPageWithLogin(LoginView):
    template_name = 'planner/landing_page.html'
    form_class = AuthenticationForm
    redirect_authenticated_user = True


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
                # return render(request, 'planner/popup.html')
            new_user = new_user[0]
            project = Project.objects.get(pk=project_id)
            project.users_list.add(new_user)
            project.save()
            projects = Project.objects.all()
            messages.info(request, "User was successfully added")
            return redirect(self.get_success_url(project_id), {'projects': projects})
        return redirect(self.get_success_url(project_id))


# Project List
class ProjectCreateView(CreateView):
    model = Project
    fields = ["title"]
    template_name = "planner/projects_listed.html"

    def get_success_url(self):
        return reverse("planner:projects_listed")

    def get_context_data(self, **kwargs):
        # display projects that they users_list contain the current logged in user
        kwargs["project_list"] = self.model.objects.filter(users_list=self.request.user)
        return super(ProjectCreateView, self).get_context_data(**kwargs)

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
        context["users_list"] = Project.objects.get(id=pk).users_list.all()
        return context

    def project_id(self):
        # allows html to access project_id through: {{ view.project_id }}
        pk = self.kwargs.get("project_id")
        return pk

    def project_title(self):
        project = self.get_project()
        return project.title

    def get_project(self):
        pk = self.kwargs.get("project_id")
        return get_object_or_404(Project, id=pk)

    def creator_username(self):
        project = self.get_project()
        return project.creator.username

    # overriding form_valid method in createView to auto populate fields
    def form_valid(self, form):
        form.instance.project = self.get_project()
        return super(ProjectWithCategoryCreate, self).form_valid(form)


# Category Deletion
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


# ----------- Task
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
            curr_user = request.user
            new_task = Task(text=text, category=category, author=curr_user)
            new_task.save()
            return redirect(self.get_success_url(project_id))


class TaskDelete(DeleteView):
    model = Task

    def get_success_url(self):
        return reverse('planner:project_page', args=(self.kwargs["project_id"],))

    def get_object(self, **kwargs):
        pk = self.kwargs.get("task_id")
        return get_object_or_404(Task, id=pk)

    def get(self, *args, **kwargs):
        return self.delete(*args, **kwargs)


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

class UserProfile(View):
    model = User

    def get(self, request, *args, **kwargs):
        pass
# USER PROFILE
# def UserProfile(request):
#     user = request.user
#     return render(request, 'planner/profile_page.html', context={'user':user})

def user_profile(request, *args, **kwargs):
    colleagues = set()
    user = request.user
    projects = Project.objects.filter(users_list__in=[user, ])
    # my_model.objects.filter(creator__in=creator_list)
    for project in projects:
        for colleague in project.users_list.all():
            colleagues.add(colleague)
    number_of_colleagues = len(colleagues)

    number_of_projects = len(projects.filter())
    first_four_projects = projects[:4]

    stock_pictures = [
        "https://images.unsplash.com/photo-1573641287741-f6e223d81a0f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1500&q=80",
        "https://res.cloudinary.com/mhmd/image/upload/v1556294927/dose-juice-1184444-unsplash_bmbutn.jpg",
        "https://res.cloudinary.com/mhmd/image/upload/v1556294926/cody-davis-253925-unsplash_hsetv7.jpg",
        "https://res.cloudinary.com/mhmd/image/upload/v1556294928/tim-foster-734470-unsplash_xqde00.jpg",
    ]

    proj_and_pics = zip(first_four_projects, stock_pictures)

    return render(request, 'planner/profile_page.html',
                  context={'user': user, 'number_of_projects': number_of_projects, 'projects': projects,
                           'first_four_projects': first_four_projects, 'stock_pictures': stock_pictures,
                           'proj_and_pics': proj_and_pics, 'colleagues': colleagues,
                           'number_of_colleagues': number_of_colleagues})
