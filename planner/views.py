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


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
    )
    

def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')

    context = {
        'form':form,
    }
    return render(request, 'planner/login.html', context)


def register_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect('/')

    context = {
        'form': form,
    }
    return render(request, "planner/signup.html", context)


def logout_view(request):
    logout(request)
    return redirect('/')
    def taskpost(self, request):
        form = TaskForm(request.POST or None)
        if form.is_valid():
            form.save()

        return render(request, '', {"form": form})

# class TaskCreate(CreateView):
#     model = Task
#     fields = ["text", "author"]


