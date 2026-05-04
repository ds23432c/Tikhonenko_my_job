from django.urls import path
from . import views
app_name = 'projects'
urlpatterns = [
    path('', views.projects_list, name='list'),
    path('<int:pk>/', views.project_detail, name='detail'),
    path('new/', views.project_create, name='create'),
    path('<int:pk>/edit/', views.project_edit, name='edit'),
    path('<int:pk>/archive/', views.project_archive, name='archive'),
]
