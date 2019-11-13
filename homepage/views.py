from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from django.contrib.auth.decorators import login_required

class IndexView(generic.ListView):
    template_name = "homepage/index.html"

    def get_queryset(self):
        return HttpResponse("")

