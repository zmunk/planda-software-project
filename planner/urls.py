from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = "planner"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),

    path("add/task/", views.add_task, name="add_task"),

]