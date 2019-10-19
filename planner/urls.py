from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = "planner"

urlpatterns = [

    # /planner/
    path("", views.IndexView.as_view(), name="index"),
    # /planner/add/task/
    path("add/task/", views.TaskCreate.as_view(), name="add_task"),
    # /planner/remove/<id>/
    path("remove/<int:pk>", views.TaskDelete.as_view(), name="remove-task"),
    # /planner/<id>/
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    ###
    path("task/<int:pk>/update/", views.TaskUpdate.as_view(), name="update-task")
    ###

    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
