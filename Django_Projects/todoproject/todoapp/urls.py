from django.urls import path
from . import views

app_name = 'todoapp'

urlpatterns = [
    path('', views.TodoListView.as_view(), name='index_url'),
    path('add/', views.add_task, name="add_url"),
    path('update/<int:pk>', views.update_task, name='update_url'),
    path('delete/<int:pk>', views.delete_task, name='delete_url'),
]
