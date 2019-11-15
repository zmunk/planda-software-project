from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = "planner"

urlpatterns = [
    # /planner/dashboard
    # path("dashboard/", views.ProjectView.as_view(), name="project_page"),
    # TODO: remove "planner" from all urls

    # /planner/projects/
    path("projects/", views.project_list_view, name="projects_listed"),  # lists user's projects

    # /planner/project/<project_id>
    path("project/<int:project_id>", views.ProjectView.as_view(), name="project_page"), # TODO
    # /planner/dashboard/
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    # /planner/add/project/
    path("add/project/", views.ProjectCreate.as_view(), name="add_project"),
    # ADD CATEGORY: /planner/project/<project_id>/add/category/
    path("project/<int:project_id>/add/category/", views.CategoryCreate.as_view(), name="add_category"),

    # ADD TASK: /planner/project/<project_id>/category/<category_id>/add/task/
    path("project/<int:project_id>/category/<int:category_id>/add/task/", views.TaskCreate.as_view(), name="add_task"),
    # /planner/<task_id>/delete/
    path("project/<int:project_id>/delete/task/<int:task_id>/", views.TaskDelete.as_view(), name="delete_task"),
    # UPDATE TASK: /planner/project/<project_id>/update/task/<task_id>/
    path("project/<int:project_id>/update/task/<int:task_id>/", views.TaskUpdate.as_view(), name="update_task"),
    # TASK DETAILS: /planner/project/<project_id>/task/<task_id>/
    path("project/<int:project_id>/task/<int:pk>/", views.DetailView.as_view(), name="detail"),



]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
