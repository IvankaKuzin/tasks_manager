from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy

from tasks.models import Task, Worker, TaskType, Position

TestCase.fixtures = ["task_management.json"]

class PublicViewTest(TestCase):
    def test_task_list_anonymous(self):
        response = self.client.get(reverse("tasks:task-list"))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, "tasks/task_list.html")

    def test_worker_list_anonymous(self):
        response = self.client.get(reverse("tasks:worker-list"))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, "tasks/worker_list.html")

    def test_task_type_list_anonymous(self):
        response = self.client.get(reverse("tasks:task-type-list"))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, "tasks/task_type_list.html")

    def test_position_list_anonymous(self):
        response = self.client.get(reverse("tasks:position-list"))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, "tasks/position_list.html")


class PrivateTaskTypeTest(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(
            name="Task Type",
        )
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")

    def test_task_type_list(self):
        response = self.client.get(reverse("tasks:task-type-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_type_list.html")

        task_types = TaskType.objects.all()
        self.assertEqual(
            list(response.context["task_type_list"]),
            list(task_types[0: len(
                response.context["task_type_list"]
            )])
        )

    def test_task_type_create(self):
        data = {
            "name": "TaskType",
        }
        url = reverse_lazy("tasks:task-type-create")
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks:task-type-list"))

        task_type = TaskType.objects.get(name="TaskType")
        self.assertEqual(task_type.name, "TaskType")

    def test_task_type_update(self):
        data = {
            "name": "TaskType",
        }
        url = reverse_lazy(
            "tasks:task-type-update",
            args=[self.task_type.pk]
        )
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks:task-type-list"))

        task_type = TaskType.objects.get(pk=self.task_type.pk)
        self.assertEqual(task_type.name, "TaskType")

    def test_task_type_delete(self):
        url = reverse_lazy(
            "tasks:task-type-delete",
            args=[self.task_type.pk]
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks:task-type-list"))
        self.assertFalse(TaskType.objects.filter(pk=self.task_type.pk).exists())


class PrivatePositionTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(
            name="Position",
        )
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")

    def test_position_list(self):
        response = self.client.get(reverse("tasks:position-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/position_list.html")

        position = Position.objects.all()
        self.assertEqual(
            list(response.context["position_list"]),
            list(position[0: len(
                response.context["position_list"]
            )])
        )

    def test_position_create(self):
        data = {
            "name": "Position name",
        }
        url = reverse_lazy("tasks:position-create")
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks:position-list"))

        position = Position.objects.get(name="Position name")
        self.assertEqual(position.name, "Position name")

    def test_position_update(self):
        data = {
            "name": "position name",
        }
        url = reverse_lazy(
            "tasks:position-update",
            args=[self.position.pk]
        )
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks:position-list"))

        position = Position.objects.get(pk=self.position.pk)
        self.assertEqual(position.name, "position name")

    def test_position_delete(self):
        url = reverse_lazy(
            "tasks:position-delete",
            args=[self.position.pk]
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks:position-list"))
        self.assertFalse(Position.objects.filter(pk=self.position.pk).exists())


class PrivateWorkerTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(
            name="Position",
        )
        self.worker = Worker.objects.create_user(
            username="newuser", password="12345",
            positions=self.position
        )
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")

    def test_worker_list(self):
        response = self.client.get(reverse("tasks:worker-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/worker_list.html")

        worker = Worker.objects.all()
        self.assertEqual(
            list(response.context["worker_list"]),
            list(worker[0: len(
                response.context["worker_list"]
            )])
        )

    def test_worker_detail(self):
        response = self.client.get(reverse(
            "tasks:worker-detail",
            args=[self.worker.pk]
        ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/worker_detail.html")

        worker = Worker.objects.get(pk=self.worker.pk)
        self.assertEqual(
            str(response.context["worker"]),
            str(worker)
        )

    def test_worker_create(self):
        data = {
            "username": "newtestuser",
            "password1": "strongpassword",
            "password2": "strongpassword",
            "first_name": "Test",
            "last_name": "Test",
            "positions": [self.position.pk]
        }
        url = reverse_lazy("tasks:worker-create")
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks:worker-list"))

        worker = Worker.objects.get(username="newtestuser")
        self.assertEqual(worker.username, "newtestuser")

    def test_worker_update(self):
        data = {
            "username": "newtestuser",
            "first_name": "Test",
            "last_name": "Test",
            "positions": [self.position.pk]
        }
        url = reverse_lazy(
            "tasks:worker-update",
            args=[self.worker.pk]
        )
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("tasks:worker-list"))

        worker = Worker.objects.get(pk=self.worker.pk)
        self.assertEqual(worker.first_name, "Test")
        self.assertEqual(worker.last_name, "Test")
        self.assertEqual(worker.username, "newtestuser")

    def test_worker_delete(self):
        url = reverse_lazy(
            "tasks:worker-delete",
            args=[self.worker.pk]
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks:worker-list"))
        self.assertFalse(Worker.objects.filter(pk=self.worker.pk).exists())


class PrivateTaskTest(TestCase):
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

    def test_task_list(self):
        response = self.client.get(reverse("tasks:task-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_list.html")

        task = Task.objects.all()
        self.assertEqual(
            list(response.context["task_list"]),
            list(task[0: len(
                response.context["task_list"]
            )])
        )

    def test_task_detail(self):
        response = self.client.get(reverse(
            "tasks:task-detail",
            args=[self.task.pk]
        ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_detail.html")

        task = Task.objects.get(pk=self.task.pk)
        self.assertEqual(
            str(response.context["task"]),
            str(task)
        )

    def test_task_create(self):
        data = {
            "name": "New task",
            "description": "New description",
            "deadline": "2025-12-31",
            "priority": "P2",
            "task_type": self.task_type.id,
            "assignees": [self.user.id]
        }
        url = reverse_lazy("tasks:task-create")
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks:task-list"))

        task = Task.objects.get(name="New task")
        self.assertEqual(task.name, "New task")

    def test_task_update(self):
        data = {
            "name": "New task",
            "description": "New description",
            "deadline": "2025-12-31",
            "priority": "P2",
            "task_type": self.task_type.id,
            "assignees": [self.user.id]
        }
        url = reverse_lazy(
            "tasks:task-update",
            args=[self.task.pk]
        )
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("tasks:task-list"))

        task = Task.objects.get(pk=self.task.pk)
        self.assertEqual(task.name, "New task")
        self.assertEqual(task.priority, "P2")
        self.assertEqual(task.task_type, self.task_type)

    def test_task_delete(self):
        url = reverse_lazy(
            "tasks:task-delete",
            args=[self.task.pk]
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks:task-list"))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

