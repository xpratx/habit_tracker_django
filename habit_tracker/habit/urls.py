from django.urls import path
from . import views
from users import views as UserViews

urlpatterns = [
    path('', views.home, name='habit-home'),
    path('about/', views.about, name='habit-about'),
    path('analytics/', views.analytics, name='habit-analytics'),
    path('daily_tracker/', views.daily_tracker, name='habit-daily_tracker'),
    path('edits/', UserViews.habit_edit_page, name='habit-edits'),
    path('edits/add/', UserViews.add_habit, name='add-habit'),
    path('edits/<int:habit_id>/delete/', UserViews.delete_habit, name='delete-habit'),
    path('edits/<int:habit_id>/edit/', UserViews.edit_habit, name='edit-habit'),
]
