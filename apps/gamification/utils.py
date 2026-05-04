from .models import Achievement, UserAchievement


def check_achievements(user):
    new_achievements = []
    try:
        profile = user.game_profile
    except:
        return new_achievements

    earned_ids = set(UserAchievement.objects.filter(user=user).values_list('achievement_id', flat=True))
    all_achievements = Achievement.objects.filter(is_active=True)

    for ach in all_achievements:
        if ach.id in earned_ids:
            continue
        earned = False
        ct = ach.condition_type
        cv = ach.condition_value

        if ct == 'tasks_completed' and profile.tasks_completed >= cv:
            earned = True
        elif ct == 'streak' and profile.streak >= cv:
            earned = True
        elif ct == 'pomodoros' and profile.pomodoros_completed >= cv:
            earned = True
        elif ct == 'level' and profile.level >= cv:
            earned = True
        elif ct == 'xp' and profile.xp >= cv:
            earned = True

        if earned:
            UserAchievement.objects.create(user=user, achievement=ach)
            profile.add_xp(ach.xp_reward)
            profile.coins += ach.coins_reward
            profile.save()
            new_achievements.append(ach)

    return new_achievements


def generate_daily_quests(user):
    from datetime import date
    from .models import DailyQuest
    today = date.today()
    if DailyQuest.objects.filter(user=user, date=today).exists():
        return
    quests = [
        {'title': 'Утренний старт', 'description': 'Выполни 3 задачи', 'quest_type': 'complete_tasks', 'target_value': 3, 'xp_reward': 30, 'coins_reward': 15},
        {'title': 'Помодоро-марафон', 'description': 'Заверши 2 помодоро', 'quest_type': 'pomodoros', 'target_value': 2, 'xp_reward': 20, 'coins_reward': 10},
        {'title': 'Планировщик', 'description': 'Создай 1 новую задачу', 'quest_type': 'create_tasks', 'target_value': 1, 'xp_reward': 10, 'coins_reward': 5},
    ]
    for q in quests:
        DailyQuest.objects.create(user=user, date=today, **q)
