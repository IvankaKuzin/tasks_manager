from django.urls import path
from tasks.views import (
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    task_update_status,
    TaskDeleteView,
    WorkerListView,
    WorkerDetailView,
    WorkerCreateView,
    WorkerUpdateView,
    WorkerDeleteView,
    TaskTypeListView,
    TaskTypeCreateView,
    TaskTypeUpdateView,
    TaskTypeDeleteView,
    PositionListView,
    PositionCreateView,
    PositionUpdateView,
    PositionDeleteView,
    TagsListView,
    TagsCreateView,
    TagsUpdateView,
    TagsDeleteView,
)

urlpatterns = [
    path("", TaskListView.as_view(), name="task-list"),
    path("<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("task-create/", TaskCreateView.as_view(), name="task-create"),
    path("<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path(
        "<int:pk>/update-status/",
        task_update_status,
        name="task-update-status",
    ),
    path("<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),

    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("workers/<int:pk>/update/", WorkerUpdateView.as_view(), name="worker-update"),
    path("workers/<int:pk>/delete/", WorkerDeleteView.as_view(), name="worker-delete"),

    path("task-types/", TaskTypeListView.as_view(), name="task-type-list"),
    path("task-types/create/", TaskTypeCreateView.as_view(), name="task-type-create"),
    path("task-types/<int:pk>/update/", TaskTypeUpdateView.as_view(), name="task-type-update"),
    path("task-types/<int:pk>/delete/", TaskTypeDeleteView.as_view(), name="task-type-delete"),

    path("positions/", PositionListView.as_view(), name="position-list"),
    path("positions/create/", PositionCreateView.as_view(), name="position-create"),
    path("positions/<int:pk>/update/", PositionUpdateView.as_view(), name="position-update"),
    path("positions/<int:pk>/delete/", PositionDeleteView.as_view(), name="position-delete"),

    path("tags/", TagsListView.as_view(), name="tag-list"),
    path("tags/create/", TagsCreateView.as_view(), name="tag-create"),
    path("tags/<int:pk>/update/", TagsUpdateView.as_view(), name="tag-update"),
    path("tags/<int:pk>/delete/", TagsDeleteView.as_view(), name="tag-delete"),
]

app_name = "tasks"
