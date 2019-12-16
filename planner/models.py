from django.db import models, transaction
from django.urls import reverse
from django.conf import settings
# from django.contrib.auth.models import User
from registration.models import User

from django.db.models import F, Max


class Project(models.Model):
    title = models.CharField(max_length=1000)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, default="", on_delete=models.CASCADE)
    users_list = models.ManyToManyField(User, related_name='users_list')
    private = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} by {self.creator}"

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


class StepManager(models.Manager):
    """ Manager to encapsulate bits of business logic """

    def move(self, obj, new_order):
        """ Move an object to a new order position """

        qs = self.get_queryset()

        with transaction.atomic():
            if obj.order > int(new_order):
                qs.filter(
                    category=obj.category,
                    order__lt=obj.order,
                    order__gte=new_order,
                ).exclude(
                    pk=obj.pk
                ).update(
                    order=F('order') + 1,
                )
            else:
                qs.filter(
                    category=obj.category,
                    order__lte=new_order,
                    order__gt=obj.order,
                ).exclude(
                    pk=obj.pk,
                ).update(
                    order=F('order') - 1,
                )

            obj.order = new_order
            obj.save()

    def create(self, **kwargs):
        instance = self.model(**kwargs)

        with transaction.atomic():
            # Get our current max order number
            results = self.filter(
                category=instance.category
            ).aggregate(
                Max('order')
            )

            # Increment and use it for our new object
            current_order = results['order__max']
            if current_order is None:
                current_order = 0

            value = current_order + 1
            print("task order: " + value)
            instance.order = value
            instance.save()

            return instance

    class Meta:
        index_together = ('category', 'order')
        # This will create a multi-column index by
        # Task ID and the order which will make this
        # query fast
        # Step.objects.filter(task=<TaskObj>).order_by('order').


class Task(models.Model):
    text = models.CharField(max_length=1000)
    category = models.ForeignKey(Category, default="", on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default="", on_delete=models.CASCADE)
    order = models.IntegerField(default=1)

    def __str__(self):
        return f"Task by {self.author}"

    def get_absolute_url(self):
        # refresh page
        return reverse("planner:detail", kwargs={"pk": self.pk})

    def get_queryset(self):
        return self.objects.order_by('order')



