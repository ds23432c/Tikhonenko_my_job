from django.contrib import admin
from .models import Task, SubTask, Tag, PomodoroSession

class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 0

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'priority', 'status', 'deadline', 'created_at']
    list_filter = ['status', 'priority']
    search_fields = ['title', 'user__username']
    inlines = [SubTaskInline]

admin.site.register(Tag)
admin.site.register(PomodoroSession)
