from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = "authentic"

urlpatterns = [

    # /auth/login
    path("login", views.login_view, name ="login_view"),
    # /auth/signup
    path('signup', views.signup_view, name="signup_view"),
    # /auth/logout
    path('logout', views.logout_view, name="logout_view"),
   
]