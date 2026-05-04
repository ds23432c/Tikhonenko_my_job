from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            from apps.gamification.models import GameProfile
            GameProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}! Начни покорять задачи! 🚀')
            return redirect('core:dashboard')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Update streak
            try:
                profile = user.game_profile
                profile.update_streak()
            except:
                pass
            messages.success(request, f'С возвращением, {user.username}! 👋')
            return redirect(request.GET.get('next', 'core:dashboard'))
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('core:home')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлён!')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user)
    from apps.tasks.models import Task
    from apps.gamification.models import UserAchievement
    stats = {
        'total_tasks': Task.objects.filter(user=request.user).count(),
        'done_tasks': Task.objects.filter(user=request.user, status='done').count(),
        'achievements': UserAchievement.objects.filter(user=request.user).count(),
    }
    return render(request, 'accounts/profile.html', {'form': form, 'stats': stats})
