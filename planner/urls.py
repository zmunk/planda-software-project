from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = "planner"

urlpatterns = [

    # /planner/
    path("", views.ProjectView.as_view(), name="project_page"),
    # /planner/dashboard/
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    # /planner/add/task/
    path("add/task/", views.TaskCreate.as_view(), name="add_task"),
    # /planner/remove/<id>/
    path("task/<int:pk>/delete/", views.TaskDelete.as_view(), name="remove-task"),
    # /planner/<id>/
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # /planner/task/<id>/update/
    path("task/<int:pk>/update/", views.TaskUpdate.as_view(), name="update-task"),
    # /planner/add/category/
    path("add/category/", views.CategoryCreate.as_view(), name="add_category"),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
