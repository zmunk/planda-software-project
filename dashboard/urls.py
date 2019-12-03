from django.urls import path
from . import views
from django.views.generic import TemplateView
app_name = "dashboard"

urlpatterns = [

    path("", views.DashboardView.as_view(), name="dashboard"),

    ]