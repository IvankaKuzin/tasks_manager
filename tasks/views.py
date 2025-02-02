from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from tasks.models import Task, Worker


# @login_required
# def index(request):
#     return render(request, "tasks/home_page.html")

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "tasks/task_list.html"
    paginate_by = 5


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = "task"
    template_name = "tasks/task_detail.html"


class WorkerListView(LoginRequiredMixin, ListView):
    model = Worker
    context_object_name = "worker_list"
    template_name = "tasks/worker_list.html"
    paginate_by = 3


class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = Worker
    context_object_name = "worker"
    template_name = "tasks/worker_detail.html"
