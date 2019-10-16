from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = "planner"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),

    path("add", views.TaskCreate.as_view(), name="task-add"),
    path("add/task/", views.add_task, name="add_task"),
    path("remove/<int:id>", views.remove_task, name="remove-task"),

    
]