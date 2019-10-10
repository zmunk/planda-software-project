from django.shortcuts import render
from django.views import generic
from .models import Task
from django.views.generic.edit import CreateView


class IndexView(generic.ListView):
    template_name = "planner/index.html"
    context_object_name = "task_list"

    def get_queryset(self):
        return Task.objects.all()


class TaskCreate(CreateView):
    model = Task
    fields = ["text", "author"]

    # process form data
    # def post(self, request):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         user = form.save(commit=False)
    #
    #         # clean (normalized data)
    #         username = form.cleaned_data["username"]
    #         password = form.cleaned_data["password"]
    #         user.set_password(password)
    #         user.save()
    #
    #         # returns User objects if credentials are correct
    #         user = authenticate(username=username, password=password)
    #         if user is not None:
    #             if user.is_active:
    #                 login(request, user)
    #                 return redirect("music:index")
    #
    #     return render(request, self.template_name, {"form": form})

