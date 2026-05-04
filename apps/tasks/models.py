from django.db import models
from apps.accounts.models import User


class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20, default='#6C63FF')
    def __str__(self): return self.name
    class Meta: unique_together = ['user', 'name']


class Task(models.Model):
    PRIORITY_CHOICES = [('low','Низкий'),('medium','Средний'),('high','Высокий'),('urgent','Срочный')]
    STATUS_CHOICES = [('todo','К выполнению'),('in_progress','В работе'),('paused','На паузе'),('done','Выполнено')]
    MATRIX_CHOICES = [('important_urgent','Важно + Срочно'),('important_not_urgent','Важно, не срочно'),('not_important_urgent','Срочно, не важно'),('not_important_not_urgent','Не важно, не срочно')]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    project = models.ForeignKey('projects.Project', on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    matrix = models.CharField(max_length=30, choices=MATRIX_CHOICES, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    scheduled_date = models.DateField(null=True, blank=True)
    scheduled_time = models.TimeField(null=True, blank=True)
    estimated_minutes = models.IntegerField(default=0)
    actual_minutes = models.IntegerField(default=0)
    xp_reward = models.IntegerField(default=10)
    is_pinned = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_overdue(self):
        if self.deadline and self.status != 'done':
            from django.utils import timezone
            return timezone.now() > self.deadline
        return False

    def complete(self):
        from django.utils import timezone
        self.status = 'done'
        self.completed_at = timezone.now()
        self.save()
        try:
            profile = self.user.game_profile
            bonus = {'urgent':25,'high':20,'medium':10,'low':5}.get(self.priority,10)
            profile.add_xp(bonus)
            profile.tasks_completed += 1
            profile.save()
            from apps.gamification.utils import check_achievements
            check_achievements(self.user)
        except Exception: pass

    def __str__(self): return self.title
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-is_pinned', '-created_at']


class SubTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    title = models.CharField(max_length=200)
    is_done = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    class Meta: ordering = ['order']
    def __str__(self): return self.title


class PomodoroSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pomodoros')
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True, related_name='pomodoros')
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(default=25)
    completed = models.BooleanField(default=False)
    class Meta: ordering = ['-started_at']
