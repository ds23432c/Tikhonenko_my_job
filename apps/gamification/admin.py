from django.contrib import admin
from .models import Achievement, UserAchievement, GameProfile, ShopItem, DailyQuest

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['icon', 'title', 'category', 'condition_type', 'condition_value', 'xp_reward', 'is_active']
    list_filter = ['category', 'is_active']

@admin.register(GameProfile)
class GameProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'level', 'xp', 'coins', 'streak', 'tasks_completed']
    ordering = ['-xp']

admin.site.register(ShopItem)
admin.site.register(DailyQuest)
admin.site.register(UserAchievement)
