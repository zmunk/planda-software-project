from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = "planner"

urlpatterns = [
    # /planner/dashboard
    # path("dashboard/", views.ProjectView.as_view(), name="project_page"), # TODO: should show us dashboard
    # TODO: remove "planner" from all urls

    # /planner/projects/
    path("projects/", views.ProjectsListed.as_view(), name="projects_listed"),  # lists user's projects

    # TODO: rewrite
    # /planner/project/<id>
    path("project/<int:pk>", views.ProjectView.as_view(), name="project_page"),
    # /planner/dashboard/
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    # /planner/add/project/
    path("add/project/", views.ProjectCreate.as_view(), name="add_project"),
    # ADD CATEGORY: /planner/project/<project_id>/add/category/
    path("project/<int:project_id>/add/category/", views.CategoryCreate.as_view(), name="add_category"),

    # ADD TASK: /planner/add/task/<category_id>/
    path("project/<int:project_id>/category/<int:category_id>/add/task/", views.TaskCreate.as_view(), name="add_task"), ##TODO
    #pass both vairables to url
    #take both variables at the end
    # /planner/<task_id>/delete/
    path("project/<int:project_id>/delete/task/<int:task_id>/", views.TaskDelete.as_view(), name="delete_task"),
    # /planner/<id>/
    path("project/<int:project_id>/task/<int:pk>/", views.DetailView.as_view(), name="detail"),
    # /planner/task/<id>/update/
    path("project/<int:project_id>/update/task/<int:task_id>/", views.TaskUpdate.as_view(), name="update_task"),



]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
