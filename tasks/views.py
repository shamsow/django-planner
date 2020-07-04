from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from .forms import TaskForm
from .models import Task
from dashboard.models import Activity
# Create your views here.
def home(request):
    user_id = request.user.id
    objs = Task.objects.filter(profile_id=user_id)
    # Get a set of all the unique dates
    dates = set([i['date'] for i in Task.objects.filter(profile_id=user_id).values('date')])
    # Create a list of queryset objects divided by date
    divisions = [objs.filter(date=i) for i in dates]
    context = {
        "divs": divisions
    }
    return render(request, "tasks/tasks_home.html", context)

def create_task(request):
    form = TaskForm(request.POST or None)
    if form.is_valid():
        user_id = request.user.id
        new_task = form.save(commit=False)
        # Try to get the activity row for the current date, otherwise create it
        try:
            activity = Activity.objects.get(profile_id= user_id, date=new_task.date)
        except:
            activity = Activity.objects.create(profile_id=user_id, date=new_task.date)
            activity.save()
        # Add the remaining fields to the task and save
        new_task.profile_id = user_id
        new_task.activity = activity
        new_task.save()
        return redirect("task_home")
    context = {
        'form': form
    }
    return render(request, "tasks/create_task.html", context)

def task_detail(request, id):
    if request.method == "POST":
        Task.objects.filter(id=id).update(completed=True)
        return redirect('task_home')
    obj = get_object_or_404(Task, id=id)
    context = {
        "task": obj
    }
    return render(request, "tasks/task_detail.html", context)


def task_update(request, id):
    ## Currently malfunctioning for some reason
    ## The object should be getting updated by this method but it creates a new object with the changed parameters
    instance = get_object_or_404(Task, id=id)
    form = TaskForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        # updated_task = form.save(commit=False)
        # instance.update(title=updated_task.title, description=updated_task.description, time=updated_task.time, date=updated_task.date, priority=updated_task.priority) 
    
        return redirect("task_home")
    context = {
        'form': form
    }
    return render(request, "tasks/task_update.html", context)


def task_delete(request, id):
    obj = get_object_or_404(Task, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect("task_home")
    context = {
        "task": obj
    }
    return render(request, "tasks/task_delete.html", context)