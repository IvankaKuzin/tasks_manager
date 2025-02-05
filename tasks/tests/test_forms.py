from django import forms
from django.test import TestCase
from django.contrib.auth import get_user_model

from tasks.forms import (
    WorkerSearchUsernameForm,
    TaskSearchForm,
    TaskTypeSearchForm,
    PositionSearchForm,
    CustomLoginForm,
    TagSearchForm,
)
from tasks.models import Task, Worker, TaskType, Position, Tag


class CustomLoginFormTest(TestCase):
    def setUp(self):
        self.form = CustomLoginForm()

    def test_remember_me_field_exists(self):
        self.assertIn("remember_me", self.form.fields)

    def test_remember_me_field_is_checkbox(self):
        self.assertIsInstance(
            self.form.fields["remember_me"].widget, forms.CheckboxInput
        )

    def test_remember_me_field_has_correct_label(self):
        self.assertEqual(self.form.fields["remember_me"].label, "Remember me")

    def test_remember_me_field_is_not_required(self):
        self.assertFalse(self.form.fields["remember_me"].required)

    def test_remember_me_field_has_correct_class(self):
        self.assertIn(
            "form-check-input",
            self.form.fields["remember_me"].widget.attrs.get("class", ""),
        )


class SearchFormsTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(
            name="Position",
        )
        self.tag = Tag.objects.create(
            name="Tag",
        )
        self.task_type = TaskType.objects.create(
            name="Task Type",
        )
        self.worker = Worker.objects.create_user(
            username="newuser", password="12345", positions=self.position
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
        self.task.tags.add(self.tag)
        self.task.save()

        self.client.login(username="testuser", password="testpass123")

    def test_worker_search(self):
        form_data = {
            "search_field": "username",
            "search_query": "newuser",
            "position": None,
            "ordering": "date_joined",
        }
        form = WorkerSearchUsernameForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_task_search(self):
        form_data = {
            "search_field": "name",
            "search_query": "Task",
            "priority": "High",
            "ordering": "deadline",
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

    def test_tag_search(self):
        form_data = {
            "name": "t",
            "ordering": "id",
        }
        form = TagSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
