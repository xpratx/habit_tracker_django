from django.contrib import admin
from .models import Profile, Habit, HabitRecord

admin.site.register(Profile)
admin.site.register(Habit)
admin.site.register(HabitRecord)

