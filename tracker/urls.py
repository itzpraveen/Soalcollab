from django.urls import path
from . import views
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('dashboard'), name='root'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('task/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('task/new/', views.create_task, name='create_task'),
    path('client/new/', views.create_client, name='create_client'),
    path('task/<int:pk>/edit/', views.TaskUpdateView.as_view(), name='update_task'),
    path('task/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='delete_task'),
    path('update_task_status/', views.update_task_status, name='update_task_status'),
]
