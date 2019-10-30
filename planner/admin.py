from django.contrib import admin
from .models import Task, Category, Project

admin.site.register(Task)
##
admin.site.register(Category)
##
admin.site.register(Project)
