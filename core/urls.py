from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, RegisterPage



urlpatterns = [
    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task-detail'),
    path('create/', TaskCreate.as_view(), name='task-create'),
    path('update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task/<int:pk>/delete/', TaskDelete.as_view(), name='task-delete'),
    path('register/', RegisterPage.as_view(), name='register'),

]

