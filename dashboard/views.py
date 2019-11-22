from django.http import HttpResponse
from django.shortcuts import render
# from django.views.generic import IndexView, FormView
from django.views import generic
from django.views.generic import TemplateView

# from .views import IndexView
# Create your views here.

class DashboardView(generic.ListView):
    template_name = "dashboard/index.html"

    def get_queryset(self):
        return HttpResponse("")
