from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LoginView
# from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from . import views
from registration import views as registration_views

app_name = "planner"

urlpatterns = [
    # LANDING PAGE AND LOGIN
    path("", views.LandingPageWithLogin.as_view(), name="landing_page"),
    # LOGOUT
    path("logout/", registration_views.logout_view, name="logout"),
    # SIGNUP
    path("register/", registration_views.register, name="register"),
    # LIST PROJECTS
    path("projects/", login_required(views.ProjectCreateView.as_view()), name="projects_listed"),
    # PROJECT PAGE
    path("project/<int:project_id>/", login_required(views.ProjectWithCategoryCreate.as_view()), name="project_page"),
    # DELETE PROJECT
    path("delete/project/<int:project_id>/", login_required(views.ProjectDeleteView.as_view()), name="delete_project"),
    # ADD TASK
    path("project/<int:project_id>/category/<int:category_id>/add/task/", login_required(views.TaskCreate.as_view()), name="add_task"),
    # DELETE TASK
    path("project/<int:project_id>/delete/task/<int:task_id>/", login_required(views.TaskDelete.as_view()), name="delete_task"),
    # UPDATE TASK
    path("project/<int:project_id>/update/task/<int:task_id>/", login_required(views.TaskUpdate.as_view()), name="update_task"),
    # ADD USER TO PROJECT
    path("project/<int:project_id>/add/user/", login_required(views.AddUserToProject.as_view()), name="add_user"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
