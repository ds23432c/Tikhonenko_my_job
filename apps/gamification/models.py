from django.db import models
from apps.accounts.models import User

LEVEL_TITLES = {1:'Новичок',2:'Стажёр',3:'Специалист',4:'Эксперт',5:'Мастер',6:'Гуру',7:'Легенда',8:'Чемпион',9:'Бог продуктивности',10:'Абсолют'}


class GameProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='game_profile')
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    coins = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)
    max_streak = models.IntegerField(default=0)
    tasks_completed = models.IntegerField(default=0)
    pomodoros_completed = models.IntegerField(default=0)
    last_active_date = models.DateField(null=True, blank=True)
    character_class = models.CharField(max_length=20, default='warrior', choices=[('warrior','Воин'),('mage','Маг'),('ninja','Ниндзя'),('archer','Лучник')])

    def xp_for_level(self, level): return level * 100
    def xp_progress_percent(self):
        needed = self.xp_for_level(self.level)
        current_level_total = sum(self.xp_for_level(i) for i in range(1, self.level))
        current_xp = self.xp - current_level_total
        return min(int((current_xp / needed) * 100), 100) if needed else 0
    def level_title(self): return LEVEL_TITLES.get(min(self.level, 10), 'Легенда')

    def add_xp(self, amount):
        self.xp += amount
        self.coins += amount // 2
        while True:
            needed = sum(self.xp_for_level(i) for i in range(1, self.level + 1))
            if self.xp >= needed: self.level += 1
            else: break
        self.save()

    def update_streak(self):
        from datetime import date, timedelta
        today = date.today()
        if self.last_active_date is None: self.streak = 1
        elif self.last_active_date == today - timedelta(days=1): self.streak += 1
        elif self.last_active_date != today: self.streak = 1
        if self.streak > self.max_streak: self.max_streak = self.streak
        self.last_active_date = today
        self.save()

    def __str__(self): return f'{self.user.username} Ур.{self.level}'
    class Meta: verbose_name = 'Игровой профиль'; verbose_name_plural = 'Игровые профили'


class Achievement(models.Model):
    CATEGORY_CHOICES = [('tasks','Задачи'),('streak','Серии'),('pomodoro','Помодоро'),('projects','Проекты'),('special','Особое')]
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=10, default='🏆')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='special')
    condition_type = models.CharField(max_length=50)
    condition_value = models.IntegerField(default=1)
    xp_reward = models.IntegerField(default=50)
    coins_reward = models.IntegerField(default=25)
    is_active = models.BooleanField(default=True)
    def __str__(self): return self.title
    class Meta: verbose_name = 'Достижение'; verbose_name_plural = 'Достижения'


class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    class Meta: unique_together = ['user', 'achievement']


class DailyQuest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_quests')
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    quest_type = models.CharField(max_length=30)
    target_value = models.IntegerField(default=1)
    current_value = models.IntegerField(default=0)
    xp_reward = models.IntegerField(default=30)
    coins_reward = models.IntegerField(default=15)
    date = models.DateField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    def progress_percent(self): return min(int((self.current_value / self.target_value) * 100), 100)
    class Meta: ordering = ['-date']


class ShopItem(models.Model):
    ITEM_TYPE_CHOICES = [('theme','Тема'),('avatar_frame','Рамка аватара'),('badge','Значок')]
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES)
    icon = models.CharField(max_length=10, default='🎨')
    price_coins = models.IntegerField(default=100)
    value = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    def __str__(self): return self.name


class UserInventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inventory')
    item = models.ForeignKey(ShopItem, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)
    is_equipped = models.BooleanField(default=False)
    class Meta: unique_together = ['user', 'item']


class LeagueEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='league_entries')
    week_start = models.DateField()
    xp_earned = models.IntegerField(default=0)
    tasks_done = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    class Meta: unique_together = ['user', 'week_start']; ordering = ['-xp_earned']
