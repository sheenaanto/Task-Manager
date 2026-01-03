from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm
from django.shortcuts import get_object_or_404


def home(request):
    """Display tasks separated into to-do and done lists with the tasks due soonest at the top."""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TaskForm()

    to_do_tasks = Task.objects.filter(is_completed=False).order_by('due_date')
    done_tasks = Task.objects.filter(is_completed=True).order_by('due_date')

    context = {
        'to_do_tasks': to_do_tasks,
        'done_tasks': done_tasks,
        'form': form,
    }

    return render(request, 'tasks/index.html', context)


def delete_task(request, task_id):
    """Delete a task by its ID."""
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('home')
