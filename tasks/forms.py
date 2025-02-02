from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from tasks.models import Task, Worker, Position


class TaskForm(forms.ModelForm):
    deadline = forms.DateField(widget = forms.SelectDateWidget)
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Task
        fields = "__all__"


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "positions",
            "first_name",
            "last_name",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['positions'].queryset = Position.objects.all()


class WorkerUpdateForm(UserChangeForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = ["username", "positions", "first_name", "last_name"]
