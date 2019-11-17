from django.shortcuts import render
# from django.views.generic import IndexView, FormView
from django.views.generic import TemplateView

# from .views import IndexView
# Create your views here.

class DashboardView(TemplateView):
    template_name = "dashboard/index.html"
