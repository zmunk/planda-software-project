from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = "planner"

urlpatterns = [

    # /planner/
    path("", views.IndexView.as_view(), name="index"),

    # path("add", views.TaskCreate.as_view(), name="task-add"),
    # /planner/add/task/
    path("add/task/", views.TaskCreate.as_view(), name="add_task"),
    # /planner/remove/1/
    path("remove/<int:id>", views.remove_task, name="remove-task"),

    
]