from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

from .models import Activity
from .forms import SignUpForm
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        dates = Activity.objects.filter(profile_id=user_id)
        # Get all the dates that contain tasks
        dates = [i for i in dates if i.task_set.all()]
        # Get all the tasks for each date
        activities = []
        for date in dates:
            activities.append(date.task_set.all())
        # Combine the dates and tasks in to a list of tuples
        plans = zip(dates, activities)
        print(plans)
        context = {
            "plans": plans
        }

        return render(request, "dashboard/dashboard.html", context)

    # Sends user to log in page if not logged in
    else:
        return render(request, "dashboard/login.html", {"message": "Please log in to add items to watchlist"})
    

def date_detail(request, slug):
    obj = get_object_or_404(Activity, date=slug)
    context = {
        "date": obj.date,
        "activity": obj.task_set.all()
    }
    
    return render(request, "dashboard/activities_detail.html", context) 


def register(request):
    # Register users with data from form
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    # Dislaying Registration form
    else:
        form = SignUpForm()
    return render(request, "dashboard/register.html", {'form': form})

def login_view(request):
    # Logging in user using built in method
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "dashboard/login.html", {"message": "Invalid credentials."})
    else:
        return render(request, "dashboard/login.html")

def logout_view(request):
    # logging out user using built in method
    logout(request)
    return render(request, "dashboard/login.html", {"message": "Logged out."})