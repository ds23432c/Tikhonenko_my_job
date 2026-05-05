from django import forms
from .models import Task, SubTask, Tag


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title', 'description', 'priority', 'status', 'matrix', 'project',
            'deadline', 'scheduled_date', 'scheduled_time', 'estimated_minutes', 'is_pinned'
        ]
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'priority': 'Приоритет',
            'status': 'Статус',
            'matrix': 'Матрица',
            'project': 'Проект',
            'deadline': 'Дедлайн',
            'scheduled_date': 'Дата',
            'scheduled_time': 'Время',
            'estimated_minutes': 'План, мин.',
            'is_pinned': 'Закрепить',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Что нужно сделать?'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Подробности...'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'matrix': forms.Select(attrs={'class': 'form-select'}),
            'project': forms.Select(attrs={'class': 'form-select'}),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'scheduled_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'scheduled_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'estimated_minutes': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.projects.models import Project
        self.fields['project'].queryset = Project.objects.filter(user=user)
        self.fields['project'].required = False
        self.fields['matrix'].required = False
        self.fields['deadline'].required = False
        self.fields['scheduled_date'].required = False
        self.fields['scheduled_time'].required = False


class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = ['title']
        labels = {
            'title': 'Название',
        }
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Подзадача...'})}
