from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = "authentic"

urlpatterns = [
    path("login", views.login_view, name ="login_view"),
    path('signup', views.signup_view, name="signup_view"),
    path('logout', views.logout_view),
   
]