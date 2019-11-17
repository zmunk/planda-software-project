from django.shortcuts import render
from django.views.generic import FormView
# Create your views here.

class DashboardView(FormView):
    template_name = "dashboard/index.html"
