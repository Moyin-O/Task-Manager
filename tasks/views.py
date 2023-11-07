# tasks/views.py
from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm
from django.contrib.auth import login
from .forms import UserRegistrationForm
import pickle
from django.core.exceptions import ObjectDoesNotExist

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')  # Replace 'home' with the URL name of your home page
    else:
        form = UserRegistrationForm()
    return render(request, 'tasks/registration.html', {'tasks': task_list, 'form': form})

def task_list(request):
   print("task_list view called")
   tasks = Task.objects.all()
   form = TaskForm()

   if request.method == 'POST':
       form = TaskForm(request.POST)
       if form.is_valid():
           if request.user.is_authenticated:
               task = form.save(commit=False)
               task.user = request.user # Assign the logged-in user to the task
               task.save()
               return redirect('task_list') # Redirect to the task list after creating a task
           else:
               # Redirect unauthenticated users to the login page
               return redirect('task_list')

   return render(request, 'tasks/task_list.html', {'tasks': tasks, 'form': form})


def view_tasks(request):
    tasks = Task.objects.all()
    form = TaskForm()

    print(request.session)  # Add this line for debugging

    # Check if an undo action is requested
    if 'undo_task_id' in request.POST:
        task_id_to_undo = request.POST['undo_task_id']
        recently_deleted_task = request.session.get('recently_deleted_task')
        if recently_deleted_task is not None:
            try:
                task_to_undo = pickle.loads(recently_deleted_task)
                task_to_undo.save() # Save the task back to the database
            except ObjectDoesNotExist:
                # Handle the case where the Task does not exist
                # For example, you could redirect the user to the task list page
                return redirect('task_list')
        else:
            # Handle the case where there is no recently deleted task in the session
            # For example, you could redirect the user to the task list page
            return redirect('task_list')

        return redirect('view_tasks') # Redirect to the view_tasks page after undoing

    # Check if a task id is provided for deletion
    if 'delete_task_id' in request.POST:
        task_id_to_delete = request.POST['delete_task_id']
        try:
            task_to_delete = Task.objects.get(pk=task_id_to_delete)
            task_to_delete.delete()

            # Store the recently deleted task ID and task in the session for undo
            request.session['recently_deleted_task_id'] = task_id_to_delete
            request.session['recently_deleted_task'] = pickle.dumps(task_to_delete)
        except ObjectDoesNotExist:
            # Handle the case where the Task does not exist
            # For example, you could redirect the user to the task list page
            return redirect('task_list')

        return redirect('view_tasks') # Redirect to the view_tasks page after deletion

    # Clear the recently deleted task ID from the session
    request.session.pop('recently_deleted_task_id', None)

    return render(request, 'tasks/view_tasks.html', {'tasks': tasks, 'form': form})
