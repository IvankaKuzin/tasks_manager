import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import Form, ModelForm

from tasks.models import Task, Worker, Position, TaskType, Tag


class CustomLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Remember me"
    )


class TaskForm(forms.ModelForm):
    deadline = forms.DateField(widget = forms.SelectDateWidget)
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
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
        help_texts = {
            "username": "Username have to be 150 characters or fewer",
            "password1": "Your password must contain at least 8 characters"
        }

    def clean_first_name(self):
        value = self.cleaned_data["first_name"]
        if not value:
            raise ValidationError("Please enter your first name.")
        if not value.isalpha():
            raise ValidationError("First name can't contain numbers or another symbols.")
        if value != value.title():
            raise ValidationError("First character in name must be upper case.")

        return value

    def clean_last_name(self):
        value = self.cleaned_data["last_name"]
        if not value:
            raise ValidationError("Please enter your last name.")
        if not value.isalpha():
            raise ValidationError("Last name can't contain numbers or another symbols.")
        if value != value.title():
            raise ValidationError("First character in last name must be upper case.")

        return value



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


class TaskTypeCreateForm(ModelForm):
    class Meta:
        model = TaskType
        fields = "__all__"

    def clean_name(self):
        name = self.cleaned_data.get("name")

        if not name:
            raise ValidationError("Name cannot be empty.")

        if not re.match(r'^[a-zA-Zа-яА-ЯёЁ\s]+$', name):
            raise ValidationError("Task name can contain only letters and spaces.")

        if name.strip() == '':
            raise ValidationError("Task name cannot be empty or contain only spaces.")

        return name


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


class PositionCreateForm(ModelForm):
    class Meta:
        model = Position
        fields = "__all__"

    def clean_name(self):
        name = self.cleaned_data.get("name")

        if not name:
            raise ValidationError("Name cannot be empty.")

        if not re.match(r'^[a-zA-Z\s]+$', name):
            raise ValidationError("Position name can contain only letters and spaces.")

        if name.strip() == '':
            raise ValidationError("Position name cannot be empty or contain only spaces.")

        return name

class TagSearchForm(Form):
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


class TagCreateForm(ModelForm):
    class Meta:
        model = Tag
        fields = "__all__"

    def clean_name(self):
        name = self.cleaned_data.get("name")

        if not name:
            raise ValidationError("Name cannot be empty.")

        if not re.match(r'^[a-zA-Z-]+$', name):
            raise ValidationError("Position name can contain only letters and ellipsis.")

        if name.strip() == '':
            raise ValidationError("Position name cannot be empty or contain only spaces.")

        return name
