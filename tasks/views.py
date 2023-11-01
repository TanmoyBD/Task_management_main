from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Task
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy
from django.core.mail import EmailMessage
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime
from accounts.models import CustomUser
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage

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
    
# class RegisterPage(FormView):
#     template_name = 'tasks/register.html'
#     form_class = UserCreationForm
#     redirect_authenticated_user = True
#     success_url = reverse_lazy('tasks')

#     def form_valid(self, form):
#         user  = form.save()
#         if user is not None:
#             login(self.request,user)
#         return super(RegisterPage, self).form_valid(form)
    
#     def get(self, *args, **kwargs):
#         if self.request.user.is_authenticated:
#             return redirect('tasks')
#         return super(RegisterPage, self).get(*args, **kwargs)


from.forms import SignupForm




def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tasks')  # Assuming you have a URL pattern named 'home'
    else:
        form = SignupForm()
    return render(request, 'tasks/register.html', {'form': form})





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

import random
def generate_confirmation_code():
    # Generate a 6-digit random number
    confirmation_code = ''.join(random.choice('0123456789') for _ in range(6))
    return confirmation_code


from accounts.models import CustomUser



def Send_mail(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            # Handle the case where the email doesn't exist
            return render(request, 'tasks/email_submit.html', {'error_message': 'Email not found'})
            
        

        confirmation_code = generate_confirmation_code()
        
        user.confirmation_code=confirmation_code
        user.save()
        
        mail_subject = 'Forgot password'
        message = f'Hi {user.username} Your verification code is: {confirmation_code}'
        to_email = email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()
        return redirect('confirmation', email=email)
    return render(request, 'tasks/email_submit.html')



# views.py

from django.shortcuts import render, redirect
from .forms import ConfirmationForm
import uuid

def Confirmation(request,email):
    if request.method == 'POST':
        form = ConfirmationForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.filter(email=email).first()
            original_code = user.confirmation_code
            user_given_code = form.cleaned_data['confirmation_code']
            print("line to 193")
            print("The code is",original_code)
            
            if original_code == user_given_code:
                random_token = str(uuid.uuid4())
                print("line to 197")
                
                # Assign the token to user.forgotten_token
                user.forgotten_token = random_token
                user.save()
                user.confirmation_code = None
                return redirect('forgot_pass',pass_rest_token=random_token)
            else:
                error = "Code is not correct"
                print("207")
                return redirect('confirmation', email=email)
    else:
        form = ConfirmationForm()

    return render(request, 'tasks/confirmation.html', {'form': form})



from django.shortcuts import render, redirect
from .models import CustomUser
from .forms import PasswordChangeForm

def Forgotten_password(request, pass_rest_token):
    try:
        
        user = CustomUser.objects.get(forgotten_token=pass_rest_token)
        print("Here are token",pass_rest_token)
    except CustomUser.DoesNotExist:
        # Handle the case where no user with the provided token is found
        # You can display an error message or redirect to an error page
        return render(request, 'tasks/error.html')  # Replace 'error.html' with your actual template

    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']

            if new_password == confirm_password:
                print("Error on 233")
                user.set_password(new_password)
                print("Error on 235")
                user.forgotten_token = None
                print("Error on 237")
                user.save()
                print("Error on 239")
                return redirect('login')
            else:
                print("Errorn on 283 ")
                return render(request, 'tasks/error.html')
    else:
        form = PasswordChangeForm()

    return render(request, 'tasks/password_change.html', {'form': form})
