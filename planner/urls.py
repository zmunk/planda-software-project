from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = "planner"

urlpatterns = [
    # /planner/
    path("dashboard/", views.ProjectView.as_view(), name="project_page"),  # TODO: should show us dashboard
    # TODO: remove "planner" from all urls

    # /planner/projects/project_name
    # path('projects/<str:project_name>/', views.ProjectView.as_view()),
    path("project/<int:pk>", views.ProjectView.as_view(), name="temp_project_page"),
    # TODO: project stored as id in url instead of name
    # /planner/dashboard/
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    # /planner/add/project/
    path("add/project/", views.ProjectCreate.as_view(), name="add_project"),

    # /planner/add/task/<id>/
    path("add/task/<int:pk>", views.TaskCreate.as_view(), name="add_task"),
    # /planner/remove/<id>/
    path("task/<int:pk>/delete/", views.TaskDelete.as_view(), name="remove-task"),
    # /planner/<id>/
    # path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # /planner/task/<id>/update/
    path("task/<int:pk>/update/", views.TaskUpdate.as_view(), name="update-task"),
    # /planner/project/<id>/add/category/
    path("projectasdf/<int:pk>/add/category/", views.CategoryCreate.as_view(), name="add_category"),  #########

    # /planner/projects/
    path("projects/", views.ProjectsListed.as_view(), name="projects_listed"),  # lists user's projects

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
