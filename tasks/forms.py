from django import forms
from tasks.models import Task, Comment


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "status", "priority", "due_date"]


class TaskFilterForm(forms.Form):
    STATUS_CHOICES = [
        ("", "All")
    ] + list(Task.STATUS_CHOICES)

    PRIORITY_CHOICES = [
        ("", "All")
    ] + list(Task.PRIORITY_CHOICES)

    DUE_DATE_CHOICES = [
        ('', 'All terms'),
        ('today', 'Today'),
        ('this_week', 'This Week'),
        ('overdue', 'Overdue')
    ]


    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, label="Статус",
                               widget=forms.Select(attrs={'class': 'form-select form-select-sm'}))
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, required=False, label="Пріорітет",
                                 widget=forms.Select(attrs={'class': 'form-select form-select-sm'}))
    due_date_period = forms.ChoiceField(choices=DUE_DATE_CHOICES, required=False, label="Термін",
                               widget=forms.Select(attrs={'class': 'form-select form-select-sm'}))
