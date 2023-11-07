from django.urls import path
from .views import task_list, view_tasks, register_user 

urlpatterns = [
   path('', task_list, name='task_list'),
   path('view-tasks/', view_tasks, name='view_tasks'),  # Add this line for the new view
   path('register/', register_user, name='register_user'),

]

from django.core.mail import send_mail

def send_deadline_email(task):
   send_mail(
       'Task Deadline Passed',
       f'The deadline for task {task.name} has passed.',
       'from@example.com',
       ['to@example.com'],
       fail_silently=False,
   )
from django.utils import timezone

def check_deadlines():
   tasks = Task.objects.filter(deadline__lt=timezone.now())
   for task in tasks:
       send_deadline_email(task)