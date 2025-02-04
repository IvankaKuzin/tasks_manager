from django.test import TestCase
from django.contrib.auth import get_user_model

from tasks.forms import (
    WorkerSearchUsernameForm,
    TaskSearchForm,
    TaskTypeSearchForm,
    PositionSearchForm,
)
from tasks.models import Task, Worker, TaskType, Position


class SearchTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(
            name="Position",
        )
        self.task_type = TaskType.objects.create(
            name="Task Type",
        )
        self.worker = Worker.objects.create_user(
            username="newuser", password="12345",
            positions=self.position
        )
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass123"
        )
        self.task = Task.objects.create(
            name="Task",
            description="Task description",
            deadline="2025-12-31",
            priority="P1",
            task_type=self.task_type,
        )
        self.task.assignees.add(self.user)
        self.task.save()

        self.client.login(username="testuser", password="testpass123")

    def test_worker_search(self):
        form_data = {
            "search_field": "username",
            "search_query": "newuser",
            "position": None,
            "ordering": "date_joined"
        }
        form = WorkerSearchUsernameForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_task_search(self):
        form_data = {
            "search_field": "name",
            "search_query": "Task",
            "priority": "High",
            "ordering": "deadline"
        }
        form = TaskSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_search(self):
        form_data = {
            "name": "Type",
            "ordering": "id",
        }
        form = TaskTypeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_position_search(self):
        form_data = {
            "name": "Pos",
            "ordering": "id",
        }
        form = PositionSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
