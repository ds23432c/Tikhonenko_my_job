from django.contrib.auth.models import AbstractUser
from django.db import models

AVATAR_CHOICES = [('🧑‍💻','Программист'),('🦸','Герой'),('🧙','Маг'),('🥷','Ниндзя'),('🤖','Робот'),('🦊','Лиса'),('🐉','Дракон'),('🚀','Астронавт')]
THEME_CHOICES = [('dark','Тёмная'),('light','Светлая'),('purple','Фиолетовая'),('ocean','Океан'),('forest','Лес'),('sunset','Закат')]


class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    avatar_emoji = models.CharField(max_length=10, default='🧑‍💻', choices=AVATAR_CHOICES)
    theme = models.CharField(max_length=20, default='dark', choices=THEME_CHOICES)
    timezone = models.CharField(max_length=50, default='Europe/Moscow')
    created_at = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_xp(self):
        try: return self.game_profile.xp
        except: return 0

    def get_level(self):
        try: return self.game_profile.level
        except: return 1

    def __str__(self): return self.username
    class Meta: verbose_name = 'Пользователь'; verbose_name_plural = 'Пользователи'
