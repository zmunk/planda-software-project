from django.db import models
from django.urls import reverse


class Category(models.Model):
    category_name = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        # go to album that was just created
        return reverse("planner-namespace:index")


class Task(models.Model):
    text = models.CharField(max_length=1000)
    author = models.CharField(max_length=100)
    category = models.ForeignKey(Category, default="", on_delete=models.CASCADE)

    def __str__(self):
        return "Task by {}".format(self.author)

    def get_absolute_url(self):
        # refresh page
        return reverse("planner-namespace:detail", kwargs={"pk": self.pk})



