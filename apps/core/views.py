from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import date, timedelta


def home(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    return render(request, 'core/home.html')


@login_required
def dashboard(request):
    from apps.tasks.models import Task
    from apps.gamification.models import DailyQuest
    from apps.gamification.utils import generate_daily_quests
    from apps.projects.models import Project

    generate_daily_quests(request.user)
    today = date.today()

    today_tasks = Task.objects.filter(
        user=request.user, scheduled_date=today
    ).order_by('scheduled_time', '-priority')

    urgent_tasks = Task.objects.filter(
        user=request.user, status__in=['todo', 'in_progress'],
        priority__in=['urgent', 'high']
    ).order_by('-priority')[:5]

    overdue_tasks = Task.objects.filter(
        user=request.user, deadline__date__lt=today,
        status__in=['todo', 'in_progress', 'paused']
    )[:3]

    recent_done = Task.objects.filter(
        user=request.user, status='done'
    ).order_by('-completed_at')[:5]

    quests = DailyQuest.objects.filter(user=request.user, date=today)
    projects = Project.objects.filter(user=request.user, is_archived=False)[:4]

    from apps.gamification.models import GameProfile
    profile, _ = GameProfile.objects.get_or_create(user=request.user)

    # Task of the day — most urgent pending
    task_of_day = Task.objects.filter(
        user=request.user, status__in=['todo', 'in_progress']
    ).order_by('-priority', 'deadline').first()

    return render(request, 'core/dashboard.html', {
        'today_tasks': today_tasks,
        'urgent_tasks': urgent_tasks,
        'overdue_tasks': overdue_tasks,
        'recent_done': recent_done,
        'quests': quests,
        'projects': projects,
        'profile': profile,
        'task_of_day': task_of_day,
        'today': today,
    })
