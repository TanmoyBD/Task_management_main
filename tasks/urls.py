from django.urls import path,include
from .views import Task_list,TaskCreate,TaskUpdate,DeleteView,CustomLoginView
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('login/',CustomLoginView.as_view(), name='login'),
    path('logout/',LogoutView.as_view(next_page='login'), name='logout'),
    path('register/',register, name='register'),
     path('', Task_list, name='tasks'),
    #path('task/<int:pk>/',TaskDetail.as_view(), name='task'),
    path('create_task/',TaskCreate.as_view(), name='create_task'),
    path('task-update/<int:pk>/',TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/',DeleteView.as_view(), name='task-delete'),
    path('complete/<int:id>/', TaskCompleted, name='task_complete'),
    path('task/<int:task_id>/', task_details, name='task_details'),
    path('completed_tasks/', get_completed_tasks, name='completed_tasks'),
    path('forgot_password/', forgot_password, name='forgot_password'),
]