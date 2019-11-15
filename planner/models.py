from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model, user_logged_in
from django.contrib.auth.models import User
from django.contrib import admin


class Project(models.Model):
    title = models.CharField(max_length=1000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default="", on_delete=models.CASCADE)
    users_list = models.ManyToManyField(User, related_name='users_list') #new
    def __str__(self):
        return self.title + " - " + str(self.user)

    def get_absolute_url(self):
        # where to go when new project is created
        return reverse("planner:projects_listed")

class Category(models.Model):
    category_name = models.CharField(max_length=250) 
    project = models.ForeignKey(Project, default="", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name + "(Category of " + self.project.title + ")"

    def get_absolute_url(self):
        # go to album that was just created
        return reverse("planner:dashboard")

    # class ArticleAdmin(admin.ModelAdmin):
    #     def save_model(self, request, obj, form, change):
    #         obj.user = request.user
    #         super().save_model(request, obj, form, change)


class Task(models.Model):
    text = models.CharField(max_length=1000)
    category = models.ForeignKey(Category, default="", on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default="", on_delete=models.CASCADE)

    def __str__(self):
        return f"Task by {self.author}"

    def get_absolute_url(self):
        # refresh page
        return reverse("planner:detail", kwargs={"pk": self.pk})


