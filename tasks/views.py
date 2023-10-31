from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Task
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy

from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime

from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

class CustomLoginView(LoginView):
    template_name = 'tasks/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')
    
class RegisterPage(FormView):
    template_name = 'tasks/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user  = form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


@login_required
def Task_list(request):
    title = request.GET.get('title')  # Get the 'title' parameter from the URL
    priority = request.GET.get('priority')  # Get the 'priority' parameter from the URL
    created_at = request.GET.get('created_at')  # Get the 'created_at' parameter from the URL
    due_date = request.GET.get('due_date')  # Get the 'due_date' parameter from the URL

    tasks = Task.objects.filter(user=request.user).order_by('priority')

    if title:
        tasks = tasks.filter(title__icontains=title)  # Filter tasks by title if provided

    if priority:
        tasks = tasks.filter(priority=priority)  # Filter tasks by priority if provided

    if created_at:
        tasks = tasks.filter(created_at__date=created_at)  # Filter tasks by creation date if provided

    if due_date:
        tasks = tasks.filter(due_date__date=due_date)  # Filter tasks by due date if provided

    count = tasks.filter(completed=False).count()

    context = {
        'tasks': tasks,
        'count': count,
        'searched_title': title,  # Pass the searched title back to the template
        'searched_priority': priority,  # Pass the searched priority back to the template
        'searched_created_at': created_at,  # Pass the searched creation date back to the template
        'searched_due_date': due_date  # Pass the searched due date back to the template
    }

    return render(request, 'tasks/task_list.html', context)


def task_details(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'tasks/task.html', {'task': task})

class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title', 'description', 'completed', 'priority', 'due_date',]
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title', 'description', 'completed', 'priority','due_date',]
    success_url = reverse_lazy('tasks')

class DeleteView(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    
    
def TaskCompleted(request, id):
    task = get_object_or_404(Task, id=id) # Assuming your model is named 'Task'
    task.completed = True  # Assuming 'completed' is a BooleanField in your model
    task.save()
    return redirect('tasks')
    
    
    
def get_completed_tasks(request):
    completed_tasks = Task.objects.filter(completed=True,user=request.user)
    context = {'completed_tasks': completed_tasks}
    return render(request, 'tasks/completed.html', context)
