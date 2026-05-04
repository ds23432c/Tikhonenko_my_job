from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'avatar_emoji', 'theme', 'is_active', 'date_joined']
    list_filter = ['theme', 'is_active']
    fieldsets = UserAdmin.fieldsets + (('Профиль', {'fields': ('bio', 'avatar_emoji', 'theme')}),)
