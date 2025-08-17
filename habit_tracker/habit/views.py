from django.shortcuts import render
from django.contrib.auth.models import User


def home(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    return render(request, 'habit/home.html', {'username' : username})

def about(request):
    return render(request, 'habit/about.html')

def daily_tracker(request):
    from habit_tracker.users.models import Habit, HabitRecord
    from datetime import date, datetime, timedelta
    from django.contrib import messages
    import calendar

    if not request.user.is_authenticated:
        return render(request, 'habit/daily_tracker.html', {'error': 'You must be logged in to view your daily tracker.'})

    # Get date from GET param, default to today
    date_str = request.GET.get('date')
    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else date.today()
    except ValueError:
        selected_date = date.today()


    habits = Habit.objects.filter(user=request.user)
    records = {r.habit_id: r for r in HabitRecord.objects.filter(habit__in=habits, date=selected_date)}

    if request.method == 'POST':
        for habit in habits:
            if habit.tracking_type == 'bool':
                checked = str(habit.id) in request.POST
                record = records.get(habit.id)
                if record:
                    if record.completed != checked:
                        record.completed = checked
                        record.save()
                else:
                    HabitRecord.objects.create(habit=habit, date=selected_date, completed=checked)
            else:
                value_str = request.POST.get(f'value_{habit.id}', '').strip()
                value = int(value_str) if value_str.isdigit() else None
                record = records.get(habit.id)
                if record:
                    record.value = value
                    record.save()
                else:
                    HabitRecord.objects.create(habit=habit, date=selected_date, value=value)
        messages.success(request, f"Progress for {selected_date.strftime('%B %d, %Y')} saved!")
        records = {r.habit_id: r for r in HabitRecord.objects.filter(habit__in=habits, date=selected_date)}

    habit_status = []
    for habit in habits:
        record = records.get(habit.id)
        if habit.tracking_type == 'bool':
            completed = record.completed if record else False
            habit_status.append({'habit': habit, 'completed': completed})
        else:
            value = record.value if record else ''
            habit_status.append({'habit': habit, 'value': value})

    prev_date = selected_date - timedelta(days=1)
    next_date = selected_date + timedelta(days=1)
    context = {
        'habit_status': habit_status,
        'today': selected_date,
        'day_name': calendar.day_name[selected_date.weekday()],
        'prev_date': prev_date,
        'next_date': next_date,
        'is_today': selected_date == date.today(),
    }
    return render(request, 'habit/daily_tracker.html', context)

def analytics(request):
    from users.models import Habit, HabitRecord
    from datetime import date, timedelta
    import calendar, json
    if not request.user.is_authenticated:
        return render(request, 'habit/analytics.html', {'error': 'You must be logged in to view analytics.'})

    today = date.today()
    week_ago = today - timedelta(days=6)
    month_ago = today - timedelta(days=29)
    habits = Habit.objects.filter(user=request.user)
    records = HabitRecord.objects.filter(habit__in=habits, date__range=(month_ago, today))
    analytics = []
    for habit in habits:
        habit_records = [r for r in records if r.habit_id == habit.id]
        week_data = []
        month_data = []
        for i in range(7):
            d = week_ago + timedelta(days=i)
            rec = next((r for r in habit_records if r.date == d), None)
            if habit.tracking_type == 'bool':
                week_data.append({'date': d.strftime('%Y-%m-%d'), 'value': 1 if (rec and rec.completed) else 0})
            else:
                week_data.append({'date': d.strftime('%Y-%m-%d'), 'value': rec.value if (rec and rec.value is not None) else 0})
        for i in range(30):
            d = month_ago + timedelta(days=i)
            rec = next((r for r in habit_records if r.date == d), None)
            if habit.tracking_type == 'bool':
                month_data.append({'date': d.strftime('%Y-%m-%d'), 'value': 1 if (rec and rec.completed) else 0})
            else:
                month_data.append({'date': d.strftime('%Y-%m-%d'), 'value': rec.value if (rec and rec.value is not None) else 0})
        analytics.append({
            'habit_id': habit.id,
            'habit_name': habit.name,
            'habit_description': habit.description,
            'tracking_type': habit.tracking_type,
            'week': week_data,
            'month': month_data,
        })
    context = {
        'analytics': analytics,
        'analytics_json': json.dumps(analytics),
        'today': today,
        'week_ago': week_ago,
        'month_ago': month_ago,
    }
    return render(request, 'habit/analytics.html', context)

def edits(request):
    return render(request, 'habit/edits.html')


