from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta, date
from apps.tasks.models import Task, PomodoroSession


@login_required
def analytics_view(request):
    user = request.user
    today = date.today()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)

    # Task stats
    all_tasks = Task.objects.filter(user=user)
    stats = {
        'total': all_tasks.count(),
        'done': all_tasks.filter(status='done').count(),
        'in_progress': all_tasks.filter(status='in_progress').count(),
        'overdue': all_tasks.filter(deadline__date__lt=today, status__in=['todo', 'in_progress', 'paused']).count(),
        'this_week': all_tasks.filter(completed_at__date__gte=week_ago, status='done').count(),
        'this_month': all_tasks.filter(completed_at__date__gte=month_ago, status='done').count(),
        'pomodoros': PomodoroSession.objects.filter(user=user, completed=True).count(),
    }

    # Completion rate
    stats['completion_rate'] = int((stats['done'] / stats['total'] * 100)) if stats['total'] > 0 else 0

    # Daily completions last 14 days
    daily_data = []
    for i in range(13, -1, -1):
        day = today - timedelta(days=i)
        count = all_tasks.filter(completed_at__date=day, status='done').count()
        daily_data.append({'date': day.strftime('%d.%m'), 'count': count})

    # Priority breakdown
    priority_data = {
        'urgent': all_tasks.filter(priority='urgent').count(),
        'high': all_tasks.filter(priority='high').count(),
        'medium': all_tasks.filter(priority='medium').count(),
        'low': all_tasks.filter(priority='low').count(),
    }

    # Top productive day of week
    from collections import Counter
    done_tasks = all_tasks.filter(status='done', completed_at__isnull=False)
    days_counter = Counter()
    days_names = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    for t in done_tasks:
        days_counter[t.completed_at.weekday()] += 1
    weekday_data = [{'day': days_names[i], 'count': days_counter.get(i, 0)} for i in range(7)]

    profile = user.game_profile
    import json
    return render(request, 'analytics/dashboard.html', {
        'stats': stats,
        'daily_data_json': json.dumps(daily_data),
        'priority_data_json': json.dumps(priority_data),
        'weekday_data_json': json.dumps(weekday_data),
        'profile': profile,
        'streak': profile.streak,
        'max_streak': profile.max_streak,
    })
