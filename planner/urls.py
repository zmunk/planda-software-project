from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = "planner"

urlpatterns = [
    # /planner/dashboard
    path("dashboard/", views.ProjectView.as_view(), name="project_page"), # TODO: should show us dashboard
    # TODO: remove "planner" from all urls

    # /planner/project/<id>
    path("project/<int:pk>", views.ProjectView.as_view(), name="temp_project_page"),
    # /planner/dashboard/
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    # /planner/add/project/
    path("add/project/", views.ProjectCreate.as_view(), name="add_project"),

    # /planner/add/task/<category_id>/
    # path("add/task/<int:pk>", views.TaskCreate.as_view(), name="add_task"),
    path("projects/<int:project_id>/add/task/<int:category_id>", views.TaskCreate.as_view(), name="add_task"), ##TODO
    #pass both vairables to url
    #take both variables at the end
    # /planner/remove/<task_id>/
    path("task/<int:pk>/delete/", views.TaskDelete.as_view(), name="remove-task"),
    # /planner/<id>/
    # path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # /planner/task/<id>/update/
    path("task/<int:pk>/update/", views.TaskUpdate.as_view(), name="update-task"),
    # /planner/project/<project_id>/add/category/
    path("project/<int:pk>/add/category/", views.CategoryCreate.as_view(), name="add_category"),

    # /planner/projects/
    path("projects/", views.ProjectsListed.as_view(), name="projects_listed"),  # lists user's projects

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
