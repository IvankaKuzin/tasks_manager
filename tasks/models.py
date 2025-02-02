from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class TaskType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    positions = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        related_name="workers",
        null=True,
    )

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def __str__(self):
        return f"{self.username} ({self.positions})"

    def get_absolute_url(self):
        return reverse("tasks:worker-detail", kwargs={"pk": self.pk})


class Task(models.Model):
    PRIORITY_LEVEL = {
        "P0": "Critical",
        "P1": "High",
        "P2": "Medium",
        "P3": "Low",
        "P4": "No priority",
    }
    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    is_complete = models.BooleanField(default=False)
    priority = models.CharField(choices=PRIORITY_LEVEL.items(), max_length=20)
    task_type = models.ForeignKey(TaskType, on_delete=models.SET_NULL, null=True)
    assignees = models.ManyToManyField(Worker, related_name="tasks")

    class Meta:
        ordering = ["deadline"]

    def __str__(self):
        return f"{self.name} - {self.task_type} ({self.priority}): {self.assignees.all()}"
