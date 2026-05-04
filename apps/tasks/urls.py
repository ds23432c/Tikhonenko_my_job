from django.urls import path
from . import views
app_name = 'tasks'
urlpatterns = [
    path('', views.task_list, name='list'),
    path('today/', views.today_view, name='today'),
    path('new/', views.task_create, name='create'),
    path('<int:pk>/', views.task_detail, name='detail'),
    path('<int:pk>/edit/', views.task_edit, name='edit'),
    path('<int:pk>/delete/', views.task_delete, name='delete'),
    path('<int:pk>/complete/', views.task_complete, name='complete'),
    path('<int:pk>/status/', views.task_status, name='status'),
    path('<int:pk>/subtask/add/', views.add_subtask, name='add_subtask'),
    path('<int:pk>/subtask/<int:subtask_pk>/toggle/', views.toggle_subtask, name='toggle_subtask'),
    path('pomodoro/', views.pomodoro_view, name='pomodoro'),
    path('pomodoro/<int:pk>/', views.pomodoro_view, name='pomodoro_task'),
    path('pomodoro/complete/', views.pomodoro_complete, name='pomodoro_complete'),
    path('<int:pk>/focus/', views.focus_mode, name='focus'),
]
