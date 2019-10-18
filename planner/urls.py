from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = "planner"

urlpatterns = [

    # /planner/
    path("", views.IndexView.as_view(), name="index"),
    # /planner/add/task/
    path("add/task/", views.TaskCreate.as_view(), name="add_task"),
    # /planner/remove/<id>/
    path("remove/<int:id>", views.remove_task, name="remove-task"),
    # /planner/<id>/
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    ###
    # path("task/<int:id>/update/", views.TaskUpdate.as_view(), name="update_task")
    ###

    
]