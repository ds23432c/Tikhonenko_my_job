import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Achievement, UserAchievement, DailyQuest, ShopItem, UserInventory, LeagueEntry, GameProfile
from .utils import generate_daily_quests
from apps.accounts.models import User
from datetime import date, timedelta


@login_required
def achievements_view(request):
    achievements = Achievement.objects.filter(is_active=True)
    earned_ids = set(UserAchievement.objects.filter(user=request.user).values_list('achievement_id', flat=True))
    return render(request, 'gamification/achievements.html', {
        'achievements': achievements,
        'earned_ids': earned_ids,
    })


@login_required
def daily_quests_view(request):
    generate_daily_quests(request.user)
    quests = DailyQuest.objects.filter(user=request.user, date=date.today())
    return render(request, 'gamification/quests.html', {'quests': quests})


@login_required
def shop_view(request):
    items = ShopItem.objects.filter(is_active=True)
    owned_ids = set(UserInventory.objects.filter(user=request.user).values_list('item_id', flat=True))
    profile = request.user.game_profile
    return render(request, 'gamification/shop.html', {
        'items': items,
        'owned_ids': owned_ids,
        'profile': profile,
    })


@login_required
@require_POST
def buy_item(request, pk):
    item = ShopItem.objects.get(pk=pk)
    profile = request.user.game_profile
    if UserInventory.objects.filter(user=request.user, item=item).exists():
        return JsonResponse({'success': False, 'error': 'Уже куплено'})
    if profile.coins < item.price_coins:
        return JsonResponse({'success': False, 'error': 'Недостаточно монет'})
    profile.coins -= item.price_coins
    profile.save()
    UserInventory.objects.create(user=request.user, item=item)
    return JsonResponse({'success': True, 'coins_left': profile.coins})


@login_required
def leaderboard_view(request):
    week_start = date.today() - timedelta(days=date.today().weekday())
    # Update current user entry
    entry, _ = LeagueEntry.objects.get_or_create(user=request.user, week_start=week_start, defaults={'xp_earned': 0})

    top_users = User.objects.filter(
        game_profile__isnull=False
    ).select_related('game_profile').order_by('-game_profile__xp')[:50]

    my_rank = User.objects.filter(game_profile__xp__gt=request.user.game_profile.xp).count() + 1

    return render(request, 'gamification/leaderboard.html', {
        'top_users': top_users,
        'my_rank': my_rank,
    })
