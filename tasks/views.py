from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.dateparse import parse_date
from tasks.forms import TaskForm, WorkerCreationForm, WorkerUpdateForm, WorkerSearchUsernameForm, TaskSearchForm, \
    TaskTypeSearchForm, PositionSearchForm, TaskTypeCreateForm, PositionCreateForm, CustomLoginForm
from tasks.models import Task, Worker, TaskType, Position
from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'registration/login.html'

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if remember_me:
            self.request.session.set_expiry(30 * 24 * 60 * 60)
        else:
            self.request.session.set_expiry(0)

        return super().form_valid(form)


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "task_list"
    paginate_by = 3
    template_name = "tasks/task_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()

        self.form = TaskSearchForm(self.request.GET)

        if self.form.is_valid():
            priority = self.form.cleaned_data.get('priority')
            if priority:
                priority_key = next(
                    (key for key, value in Task.PRIORITY_LEVEL.items() if value == priority),
                    None
                )
                if priority_key:
                    queryset = queryset.filter(priority=priority_key)

            search_field = self.form.cleaned_data.get('search_field')
            search_query = self.form.cleaned_data.get('search_query')

            if search_field and search_query:
                filter_kwargs = {}

                if search_field == 'deadline':
                    try:
                        deadline = parse_date(search_query)
                        if deadline:
                            filter_kwargs[f'{search_field}'] = deadline
                    except ValueError:
                        pass
                else:
                    filter_kwargs[f'{search_field}__icontains'] = search_query

                queryset = queryset.filter(**filter_kwargs)

            ordering = self.form.cleaned_data.get('ordering')
            if ordering:
                queryset = queryset.order_by(ordering)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form
        return context


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


def task_update_status(request, pk):
    task = Task.objects.get(id=pk)
    task.is_complete = not task.is_complete
    task.save()

    return redirect(reverse("tasks:task-list"))


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:task-list")


class WorkerListView(LoginRequiredMixin, ListView):
    model = Worker
    context_object_name = "worker_list"
    template_name = "tasks/worker_list.html"
    paginate_by = 3
    queryset = Worker.objects.select_related("positions")

    def get_queryset(self):
        queryset = super().get_queryset()

        self.form = WorkerSearchUsernameForm(self.request.GET)

        if self.form.is_valid():
            position = self.form.cleaned_data.get('position')
            if position:
                queryset = queryset.filter(positions=position)

            search_field = self.form.cleaned_data.get('search_field')
            search_query = self.form.cleaned_data.get('search_query')

            if search_field and search_query:
                filter_kwargs = {
                    f'{search_field}__icontains': search_query
                }
                queryset = queryset.filter(**filter_kwargs)

            ordering = self.form.cleaned_data.get('ordering')
            if ordering:
                queryset = queryset.order_by(ordering)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form
        return context


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


class TaskTypeListView(LoginRequiredMixin, ListView):
    model = TaskType
    context_object_name = "task_type_list"
    paginate_by = 3
    template_name = "tasks/task_type_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()

        self.form = TaskTypeSearchForm(self.request.GET)

        if self.form.is_valid():
            name = self.form.cleaned_data.get('name')
            if name:
                queryset = queryset.filter(name__icontains=name)

            ordering = self.form.cleaned_data.get('ordering')
            if ordering:
                queryset = queryset.order_by(ordering)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form
        return context


class TaskTypeCreateView(LoginRequiredMixin, CreateView):
    model = TaskType
    form_class = TaskTypeCreateForm
    context_object_name = "task_type"
    success_url = reverse_lazy("tasks:task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = TaskType
    form_class = TaskTypeCreateForm
    success_url = reverse_lazy("tasks:task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = TaskType
    success_url = reverse_lazy("tasks:task-type-list")


class PositionListView(LoginRequiredMixin, ListView):
    model = Position
    context_object_name = "position_list"
    paginate_by = 3
    template_name = "tasks/position_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()

        self.form = PositionSearchForm(self.request.GET)

        if self.form.is_valid():
            name = self.form.cleaned_data.get('name')
            if name:
                queryset = queryset.filter(name__icontains=name)

            ordering = self.form.cleaned_data.get('ordering')
            if ordering:
                queryset = queryset.order_by(ordering)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form
        return context


class PositionCreateView(LoginRequiredMixin, CreateView):
    model = Position
    form_class = PositionCreateForm
    success_url = reverse_lazy("tasks:position-list")


class PositionUpdateView(LoginRequiredMixin, UpdateView):
    model = Position
    form_class = PositionCreateForm
    success_url = reverse_lazy("tasks:position-list")


class PositionDeleteView(LoginRequiredMixin, DeleteView):
    model = Position
    success_url = reverse_lazy("tasks:position-list")
