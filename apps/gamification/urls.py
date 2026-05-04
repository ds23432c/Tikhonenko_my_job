from django.urls import path
from . import views
app_name = 'gamification'
urlpatterns = [
    path('achievements/', views.achievements_view, name='achievements'),
    path('quests/', views.daily_quests_view, name='quests'),
    path('shop/', views.shop_view, name='shop'),
    path('shop/<int:pk>/buy/', views.buy_item, name='buy'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
]
