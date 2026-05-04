from django.db import models
from apps.accounts.models import User


class Project(models.Model):
    COLOR_CHOICES = [('#6C63FF','Фиолетовый'),('#FF6584','Розовый'),('#43E97B','Зелёный'),('#FFA726','Оранжевый'),('#26C6DA','Голубой'),('#EF5350','Красный'),('#AB47BC','Лиловый'),('#FFD600','Жёлтый')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=10, choices=COLOR_CHOICES, default='#6C63FF')
    icon = models.CharField(max_length=10, default='📁')
    deadline = models.DateField(null=True, blank=True)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def progress(self):
        total = self.tasks.count()
        if total == 0: return 0
        done = self.tasks.filter(status='done').count()
        return int((done / total) * 100)

    def __str__(self): return self.name
    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-created_at']
