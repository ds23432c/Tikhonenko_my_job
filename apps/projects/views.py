from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'color', 'icon', 'deadline']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название проекта'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'color': forms.Select(attrs={'class': 'form-select'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '📁'}),
            'deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


@login_required
def projects_list(request):
    projects = Project.objects.filter(user=request.user, is_archived=False)
    archived = Project.objects.filter(user=request.user, is_archived=True)
    return render(request, 'projects/list.html', {'projects': projects, 'archived': archived})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    tasks = project.tasks.all()
    from apps.tasks.models import Task
    kanban = {
        'todo': tasks.filter(status='todo'),
        'in_progress': tasks.filter(status='in_progress'),
        'paused': tasks.filter(status='paused'),
        'done': tasks.filter(status='done'),
    }
    return render(request, 'projects/detail.html', {'project': project, 'tasks': tasks, 'kanban': kanban})


@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            messages.success(request, f'Проект «{project.name}» создан!')
            return redirect('projects:detail', pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, 'projects/form.html', {'form': form, 'title': 'Новый проект'})


@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Проект обновлён!')
            return redirect('projects:detail', pk=pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/form.html', {'form': form, 'title': 'Редактировать проект', 'project': project})


@login_required
def project_archive(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    project.is_archived = not project.is_archived
    project.save()
    messages.info(request, f'Проект {"архивирован" if project.is_archived else "восстановлен"}')
    return redirect('projects:list')
