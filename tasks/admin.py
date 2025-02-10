from django.contrib import admin

from tasks.models import Task, Worker, Position, TaskType

admin.site.register(Task)
admin.site.register(Worker)
admin.site.register(Position)
admin.site.register(TaskType)
