from django.conf.urls import url
from django.urls import path, reverse_lazy
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
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
    # USER CONFIRMATION
    # path("account_activation_sent", registration_views.account_activation_sent, name='account_activation_sent'),
    # ACTIVATING USER
    path('activate/<slug:uidb64>/<slug:token>/', registration_views.activate, name='activate'),
    # url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     registration_views.activate, name='activate'),

    # SIGNUP
    path("register/", registration_views.register, name="register"),

    # RESET PASSWORD
    path('password/reset/', PasswordResetView.as_view(template_name='registration/password_reset.html'),
         name='password_reset'),
    path('password/reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # LIST PROJECTS
    path("projects/", login_required(views.ProjectCreateView.as_view()), name="projects_listed"),
    # PROJECT PAGE
    # path("project/<int:project_id>/", login_required(views.ProjectWithCategoryCreate.as_view()), name="project_page"),
    path("project/<int:project_id>/", login_required(views.ProjectView.as_view()), name="project_page"),
    # ADD CATEGORY
    path("project/<int:project_id>/add/category/", login_required(views.CategoryCreate.as_view()), name="add_category"),
    # PROJECT UPDATE
    path("project/<int:project_id>/update", login_required(views.ProjectDataUpdate.as_view())),
    # DELETE PROJECT
    path("delete/project/<int:project_id>/", login_required(views.ProjectDeleteView.as_view()), name="delete_project"),
    # DELETE CATEGORY
    path("delete/<int:category_id>/<int:project_id>/", login_required(views.CategoryDeleteView.as_view()),
         name="delete_category"),
    # ADD TASK
    path("project/<int:project_id>/category/<int:category_id>/add/task/", login_required(views.TaskCreate.as_view()),
         name="add_task"),
    # DELETE TASK
    path("project/<int:project_id>/delete/task/<int:task_id>/", login_required(views.TaskDelete.as_view()),
         name="delete_task"),
    # UPDATE TASK
    path("project/<int:project_id>/update/task/<int:task_id>/", login_required(views.TaskUpdate.as_view()), name="edit_task"),  # TODO: this is never called
    # ADD USER TO PROJECT
    path("project/<int:project_id>/add/user/", login_required(views.AddUserToProject.as_view()), name="add_user"),
    # PROFILE PAGE
    path("user/<str:username>", views.UserProfile.as_view(), name="user_profile")
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
