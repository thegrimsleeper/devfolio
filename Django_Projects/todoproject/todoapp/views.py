from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import ListView
from .models import Task

class TodoListView(ListView):
    template_name = 'todoapp/index.html'
    model = Task
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = Task.objects.order_by("-created_at")
        return queryset
    

def add_task(request):
    if request.POST:
        Task.objects.create(task_name=request.POST['task_name'])
    return redirect('todoapp:index_url')

def update_task(request, pk):
    if request.POST:
        task = Task.objects.get(pk=pk)
        if task.is_complete:
            task.is_complete = False
        else:
            task.is_complete = True
    task.save()
    return redirect('todoapp:index_url')

def delete_task(request, pk):
    task = Task.objects.get(pk=pk)
    task.delete()
    return redirect('todoapp:index_url')