import random
from django.conf import settings


def global_context(request):
    ctx = {
        'daily_quote': random.choice(settings.DAILY_QUOTES),
    }
    if request.user.is_authenticated:
        try:
            from apps.gamification.models import DailyQuest, GameProfile
            from datetime import date
            ctx['pending_quests'] = DailyQuest.objects.filter(
                user=request.user, date=date.today(), is_completed=False
            ).count()
            ctx['user_theme'] = request.user.theme
            profile, _ = GameProfile.objects.get_or_create(user=request.user)
            ctx['game_profile'] = profile
        except Exception:
            pass
    return ctx
