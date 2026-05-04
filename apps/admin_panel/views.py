from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Sum
from datetime import date, timedelta
from apps.accounts.models import User
from apps.tasks.models import Task
from apps.gamification.models import GameProfile, Achievement


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def dashboard(request):
    today = date.today()
    week_ago = today - timedelta(days=7)
    stats = {
        'total_users': User.objects.count(),
        'new_users_week': User.objects.filter(date_joined__date__gte=week_ago).count(),
        'total_tasks': Task.objects.count(),
        'done_tasks': Task.objects.filter(status='done').count(),
        'tasks_week': Task.objects.filter(completed_at__date__gte=week_ago, status='done').count(),
    }
    top_users = User.objects.filter(game_profile__isnull=False).select_related('game_profile').order_by('-game_profile__xp')[:10]
    recent_users = User.objects.order_by('-date_joined')[:10]
    return render(request, 'admin_panel/dashboard.html', {
        'stats': stats, 'top_users': top_users, 'recent_users': recent_users,
    })


@admin_required
def users_list(request):
    users = User.objects.select_related('game_profile').order_by('-date_joined')
    return render(request, 'admin_panel/users.html', {'users': users})


@admin_required
def toggle_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.is_active = not user.is_active
    user.save()
    messages.success(request, f'Пользователь {"активирован" if user.is_active else "заблокирован"}')
    return redirect('admin_panel:users')


@admin_required
def achievements_manage(request):
    achievements = Achievement.objects.all()
    return render(request, 'admin_panel/achievements.html', {'achievements': achievements})
