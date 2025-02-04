from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import Form

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


class WorkerSearchUsernameForm(Form):
    SEARCH_FIELDS = [
        ('username', 'Username'),
        ('email', 'Email'),
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
    ]

    search_field = forms.ChoiceField(
        choices=SEARCH_FIELDS,
        required=False,
        label="Search by"
    )
    search_query = forms.CharField(
        max_length=255,
        required=False,
        label="Search query"
    )
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        required=False,
        label="Position"
    )
    ordering = forms.ChoiceField(
        choices=[
            ('username', 'Username (A-Z)'),
            ('-username', 'Username (Z-A)'),
            ('date_joined', 'Oldest'),
            ('-date_joined', 'Newest'),
        ],
        required=False,
        label="Sort by"
    )


class TaskSearchForm(Form):
    SEARCH_FIELDS = [
        ('name', 'Name'),
        ('description', 'Description'),
        ('deadline', 'Deadline'),
        ('priority', 'Priority'),
    ]

    PRIORITY_CHOICES = [
        ('', 'All Priorities'),
        *[(value, value) for value in Task.PRIORITY_LEVEL.values()]
    ]

    search_field = forms.ChoiceField(
        choices=SEARCH_FIELDS,
        required=False,
        label="Search by"
    )
    search_query = forms.CharField(
        max_length=255,
        required=False,
        label="Search query"
    )
    priority = forms.ChoiceField(
        choices=PRIORITY_CHOICES,
        required=False,
        label="Priority"
    )
    ordering = forms.ChoiceField(
        choices=[
            ("name", "Name (A-Z)"),
            ("-name", "Name (Z-A)"),
            ('deadline', 'Deadline (Earliest)'),
            ('-deadline', 'Deadline (Latest)'),
            ('-priority', 'Priority (Low to High)'),
            ('priority', 'Priority (High to Low)'),
        ],
        required=False,
        label="Sort by"
    )


class TaskTypeSearchForm(Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="Search by name"
    )
    ordering = forms.ChoiceField(
        choices=[
            ('name', 'Name (A-Z)'),
            ('-name', 'Name (Z-A)'),
            ('id', 'Oldest'),
            ('-id', 'Newest'),
        ],
        required=False,
        label="Sort by"
    )


class PositionSearchForm(Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="Search by name"
    )
    ordering = forms.ChoiceField(
        choices=[
            ('name', 'Name (A-Z)'),
            ('-name', 'Name (Z-A)'),
            ('id', 'Oldest'),
            ('-id', 'Newest'),
        ],
        required=False,
        label="Sort by"
    )
