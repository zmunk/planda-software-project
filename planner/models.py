from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model, user_logged_in
from django.contrib import admin


class Project(models.Model):
    title = models.CharField(max_length=1000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default="", on_delete=models.CASCADE)
    def __str__(self):
        return self.title + " - " + self.user.username


class Category(models.Model):
    category_name = models.CharField(max_length=250) 
    project = models.ForeignKey(Project, default="", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default="", on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name + " - " +  self.user.username

    def get_absolute_url(self):
        # go to album that was just created
        return reverse("planner-namespace:index")


    
    # class ArticleAdmin(admin.ModelAdmin):
    #     def save_model(self, request, obj, form, change):
    #         obj.user = request.user
    #         super().save_model(request, obj, form, change)



class Task(models.Model):
    text = models.CharField(max_length=1000)
    author = models.CharField(max_length=100)
    category = models.ForeignKey(Category, default="", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default="", on_delete=models.CASCADE)

    def __str__(self):
        return "Task by {}".format(self.author)

    def get_absolute_url(self):
        # refresh page
        return reverse("planner-namespace:detail", kwargs={"pk": self.pk})


