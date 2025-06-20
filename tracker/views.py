from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .models import Task, Client
from .forms import TaskForm, ClientForm

class DashboardView(ListView):
    model = Task
    template_name = 'tracker/dashboard.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Group tasks by status
        status_columns = {}
        for status in Task.Status.choices:
            status_columns[status[0]] = Task.objects.filter(status=status[0])
        context['status_columns'] = status_columns
        return context

import json

def update_task_status(request):
    if request.method == 'POST':
        task_updates = json.loads(request.POST.get('task_updates', '{}'))
        
        for task_id, new_status in task_updates.items():
            # Prevent moving tasks to 'Inbox'
            if new_status == Task.Status.INBOX:
                continue

            task = get_object_or_404(Task, id=task_id)
            task.status = new_status
            task.save()
            
        # Re-render the dashboard component
        status_columns = {}
        for status in Task.Status.choices:
            status_columns[status[0]] = Task.objects.filter(status=status[0])
        
        return render(request, 'tracker/dashboard.html', {'status_columns': status_columns})
    return HttpResponse(status=400)

def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task created successfully.')
            return redirect('dashboard')
    else:
        form = TaskForm()
    return render(request, 'tracker/create_task.html', {'form': form})

def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client created successfully.')
            return redirect('dashboard')
    else:
        form = ClientForm()
    return render(request, 'tracker/create_client.html', {'form': form})

class TaskDetailView(DetailView):
    model = Task
    template_name = 'tracker/task_detail.html'
    context_object_name = 'task'

class TaskUpdateView(SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tracker/create_task.html'
    success_url = reverse_lazy('dashboard')
    success_message = "Task updated successfully."

class TaskDeleteView(SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tracker/task_confirm_delete.html'
    success_url = reverse_lazy('dashboard')
    success_message = "Task deleted successfully."
