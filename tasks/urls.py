from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='task_home'),
    path('detail/<int:id>/', views.task_detail, name="task_detail"),
    path('create/', views.create_task, name="create_task"),
    path('update/<int:id>/', views.task_update, name="task_update"),
    path('delete/<int:id>/', views.task_delete, name="task_delete")

]