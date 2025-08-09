from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'




class Habit(models.Model):
    TRACKING_TYPE_CHOICES = [
        ('bool', 'Checkbox (Yes/No)'),
        ('int', 'Integer (Number)')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    tracking_type = models.CharField(max_length=8, choices=TRACKING_TYPE_CHOICES, default='bool')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class HabitRecord(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='records')
    date = models.DateField()
    completed = models.BooleanField(default=False)
    value = models.IntegerField(null=True, blank=True)  # For integer tracking habits

    class Meta:
        unique_together = ('habit', 'date')