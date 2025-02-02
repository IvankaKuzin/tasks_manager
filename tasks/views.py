from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from tasks.forms import TaskForm, WorkerCreationForm, WorkerUpdateForm, WorkerSearchUsernameForm, TaskSearchNameForm
from tasks.models import Task, Worker


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "tasks/task_list.html"
    paginate_by = 5
    queryset = Task.objects.select_related("task_type").prefetch_related("assignees")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskSearchNameForm(initial={"name": name})
        return context

    def get_queryset(self):
        name = self.request.GET.get("name")

        if name:
            return Task.objects.filter(name__icontains=name)
        else:
            return Task.objects.all()


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = "task"
    template_name = "tasks/task_detail.html"


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task-list")


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task-list")


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:task-list")


class WorkerListView(LoginRequiredMixin, ListView):
    model = Worker
    context_object_name = "worker_list"
    template_name = "tasks/worker_list.html"
    paginate_by = 3
    queryset = Worker.objects.select_related("positions")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = WorkerSearchUsernameForm(initial={"username": username})
        return context

    def get_queryset(self):
        username = self.request.GET.get("username")

        if username:
            return Worker.objects.filter(username__icontains=username)
        else:
            return Worker.objects.all()


class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = Worker
    context_object_name = "worker"
    template_name = "tasks/worker_detail.html"


class WorkerCreateView(LoginRequiredMixin, CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("tasks:worker-list")


class WorkerUpdateView(LoginRequiredMixin, UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    success_url = reverse_lazy("tasks:worker-list")


class WorkerDeleteView(LoginRequiredMixin, DeleteView):
    model = Worker
    success_url = reverse_lazy("tasks:worker-list")
