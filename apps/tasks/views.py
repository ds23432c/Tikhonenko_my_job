import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count
from .models import Task, SubTask, PomodoroSession
from .forms import TaskForm, SubTaskForm


@login_required
def task_list(request):
    view = request.GET.get('view', 'list')
    status_f = request.GET.get('status', '')
    priority_f = request.GET.get('priority', '')
    query = request.GET.get('q', '')
    tasks = Task.objects.filter(user=request.user).prefetch_related('subtasks', 'tags').annotate(
        done_subtasks_count=Count('subtasks', filter=Q(subtasks__is_done=True))
    )
    if status_f:
        tasks = tasks.filter(status=status_f)
    if priority_f:
        tasks = tasks.filter(priority=priority_f)
    if query:
        tasks = tasks.filter(Q(title__icontains=query) | Q(description__icontains=query))

    # Kanban grouping
    kanban = {
        'todo': tasks.filter(status='todo'),
        'in_progress': tasks.filter(status='in_progress'),
        'paused': tasks.filter(status='paused'),
        'done': tasks.filter(status='done'),
    }

    # Matrix grouping
    matrix = {
        'important_urgent': tasks.filter(matrix='important_urgent'),
        'important_not_urgent': tasks.filter(matrix='important_not_urgent'),
        'not_important_urgent': tasks.filter(matrix='not_important_urgent'),
        'not_important_not_urgent': tasks.filter(matrix='not_important_not_urgent'),
    }

    return render(request, 'tasks/list.html', {
        'tasks': tasks,
        'kanban': kanban,
        'matrix': matrix,
        'view': view,
        'status_choices': Task.STATUS_CHOICES,
        'priority_choices': Task.PRIORITY_CHOICES,
        'status_f': status_f,
        'priority_f': priority_f,
        'query': query,
        'today': timezone.now().date(),
    })


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.user, request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            # XP based on priority
            task.xp_reward = {'urgent': 25, 'high': 20, 'medium': 10, 'low': 5}.get(task.priority, 10)
            task.save()
            form.save_m2m()
            messages.success(request, f'Задача «{task.title}» создана! 📋')
            return redirect('tasks:list')
    else:
        form = TaskForm(request.user)
    return render(request, 'tasks/form.html', {'form': form, 'title': 'Новая задача'})


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    subtask_form = SubTaskForm()
    pomodoros = task.pomodoros.filter(completed=True).count()
    return render(request, 'tasks/detail.html', {
        'task': task,
        'subtask_form': subtask_form,
        'pomodoros': pomodoros,
    })


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.user, request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Задача обновлена!')
            return redirect('tasks:detail', pk=pk)
    else:
        form = TaskForm(request.user, instance=task)
    return render(request, 'tasks/form.html', {'form': form, 'title': 'Редактировать задачу', 'task': task})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
    messages.info(request, 'Задача удалена.')
    return redirect('tasks:list')


@login_required
@require_POST
def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if task.status != 'done':
        task.complete()
        return JsonResponse({'success': True, 'xp': task.xp_reward, 'level': request.user.get_level()})
    return JsonResponse({'success': False})


@login_required
@require_POST
def task_status(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    data = json.loads(request.body)
    new_status = data.get('status')
    if new_status in dict(Task.STATUS_CHOICES):
        if new_status == 'done' and task.status != 'done':
            task.complete()
        else:
            task.status = new_status
            task.save()
    return JsonResponse({'success': True})


@login_required
@require_POST
def add_subtask(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    form = SubTaskForm(request.POST)
    if form.is_valid():
        subtask = form.save(commit=False)
        subtask.task = task
        subtask.save()
        return JsonResponse({'success': True, 'id': subtask.id, 'title': subtask.title})
    return JsonResponse({'success': False})


@login_required
@require_POST
def toggle_subtask(request, pk, subtask_pk):
    subtask = get_object_or_404(SubTask, pk=subtask_pk, task__user=request.user)
    subtask.is_done = not subtask.is_done
    subtask.save()
    return JsonResponse({'success': True, 'is_done': subtask.is_done})


@login_required
def pomodoro_view(request, pk=None):
    task = None
    if pk:
        task = get_object_or_404(Task, pk=pk, user=request.user)
    tasks = Task.objects.filter(user=request.user, status__in=['todo', 'in_progress'])
    return render(request, 'tasks/pomodoro.html', {'task': task, 'tasks': tasks})


@login_required
@require_POST
def pomodoro_complete(request):
    data = json.loads(request.body)
    task_id = data.get('task_id')
    task = None
    if task_id:
        try:
            task = Task.objects.get(pk=task_id, user=request.user)
            task.actual_minutes += data.get('duration', 25)
            task.save()
        except Task.DoesNotExist:
            pass
    PomodoroSession.objects.create(
        user=request.user, task=task,
        duration_minutes=data.get('duration', 25), completed=True
    )
    profile = request.user.game_profile
    profile.add_xp(5)
    profile.pomodoros_completed += 1
    profile.save()
    from apps.gamification.utils import check_achievements
    check_achievements(request.user)
    return JsonResponse({'success': True, 'xp': 5})


@login_required
def focus_mode(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, 'tasks/focus.html', {'task': task})


@login_required
def today_view(request):
    today = timezone.now().date()
    tasks = Task.objects.filter(user=request.user, scheduled_date=today).order_by('scheduled_time', '-priority')
    overdue = Task.objects.filter(
        user=request.user, deadline__date__lt=today, status__in=['todo', 'in_progress', 'paused']
    )
    return render(request, 'tasks/today.html', {'tasks': tasks, 'overdue': overdue, 'today': today})
