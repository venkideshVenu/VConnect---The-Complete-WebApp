from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('tasks/<int:pk>/update-status/', views.update_task_status, name='update_task_status'),

    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('projects/<int:project_pk>/tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/edit/', views.task_edit, name='task_edit'),

    path('projects/<int:pk>/toggle-complete/', views.project_toggle_complete, name='project_toggle_complete'),
    path('tasks/<int:pk>/toggle-complete/', views.task_toggle_complete, name='task_toggle_complete'),
]