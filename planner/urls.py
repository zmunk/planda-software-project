from django.urls import path
from . import views

app_name = "planner"

urlpatterns = [
    # /planner/
    path("", views.IndexView.as_view(), name="index"),
    path("/add", views.TaskCreate.as_view(), name="task-add")


]