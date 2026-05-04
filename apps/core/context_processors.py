import random
from django.conf import settings


def global_context(request):
    ctx = {
        'daily_quote': random.choice(settings.DAILY_QUOTES),
    }
    if request.user.is_authenticated:
        try:
            from apps.gamification.models import DailyQuest
            from datetime import date
            ctx['pending_quests'] = DailyQuest.objects.filter(
                user=request.user, date=date.today(), is_completed=False
            ).count()
            ctx['user_theme'] = request.user.theme
            ctx['game_profile'] = request.user.game_profile
        except Exception:
            pass
    return ctx
