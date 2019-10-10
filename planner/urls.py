from django.urls import path
from . import views

app_name = "planner"

urlpatterns = [
    # /planner/
    path("", views.IndexView.as_view(), name="index"),
    path("add", views.TaskCreate.as_view(), name="task-add"),
    path("login", views.login_view, name ="login_view"),
    path('register', views.register_view, name="register_view"),
    path('logout', views.logout_view)

]