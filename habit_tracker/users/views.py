from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm  #helps to make a builtin login form
from django.contrib import messages

from .models import HabitRecord, Habit
from .forms import UserRegisterForm, HabitForm
from django.contrib.auth.decorators import login_required
from datetime import timedelta, date
from django.db.models import Count



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('habit-home')
    else:
        form = UserRegisterForm()
    
    return render(request, 'users/register.html', {'form':form})


@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
def get_habit_analytics(user, habit_id):
    # Fetch 30 days of logs
    today = date.today()
    start_day = today - timedelta(days=29)
    records = (HabitRecord.objects
        .filter(habit__user=user, habit_id=habit_id, date__range=(start_day, today))
        .order_by('date'))

    dates = [start_day + timedelta(days=i) for i in range(30)]
    analytics = {r.date: r.completed for r in records}
    data = [{'date': d, 'completed': analytics.get(d, False)} for d in dates]
    return data



@login_required
def add_habit(request):
    if request.method == "POST":
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect('habit-edits')
    else:
        form = HabitForm()
    return render(request, 'users/add_habit.html', {'form': form})

@login_required
def delete_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    if request.method == "POST":
        habit.delete()
        return redirect('habit-edits')
    return render(request, 'users/delete_habit_confirm.html', {'habit': habit})

@login_required
def edit_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    if request.method == "POST":
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            return redirect('habit-edits')
    else:
        form = HabitForm(instance=habit)
    return render(request, 'users/edit_habit.html', {'form': form, 'habit': habit})



@login_required
def habit_edit_page(request):
    # Filter habits belonging to the logged-in user
    user_habits = Habit.objects.filter(user=request.user)
    print("Habits in view")
    return render(request, 'habit/edits.html', {'habits': user_habits, 'test_var': 'Hellow World'})
