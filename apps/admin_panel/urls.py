from django.urls import path
from . import views
app_name = 'admin_panel'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('users/', views.users_list, name='users'),
    path('users/<int:pk>/toggle/', views.toggle_user, name='toggle_user'),
    path('achievements/', views.achievements_manage, name='achievements'),
]
