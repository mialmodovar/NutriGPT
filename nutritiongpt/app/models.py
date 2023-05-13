from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(default=timezone.datetime(2000, 1, 1))
    height = models.FloatField(default=175.0)  # in centimeters
    weight = models.FloatField(default=70.0)  # in kilograms
    gender = models.CharField(max_length=10, choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],default="Other")
    calories_goal = models.FloatField(default=2500.0)
    protein_goal = models.FloatField(default=343.0)
    carbohydrates_goal = models.FloatField(default=140.0)
    fats_goal = models.FloatField(default=76)
    conversation = models.JSONField(null=True, blank=True) # Store the prompt and response

    def __str__(self):
        return self.user.username

class DailyIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_counter = models.IntegerField(default=0) # Count requests made by the user in a day
    date = models.DateField(default=timezone.now) # set the default value to current date
    calories = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    carbohydrates = models.FloatField(default=0)
    fats = models.FloatField(default=0)

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class Exercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now) # set the default value to current datetime
    exercise_name = models.CharField(max_length=255)
    calories_burned = models.FloatField()

    def __str__(self):
        return f"{self.user.username} - {self.exercise_name} - {self.date}"

class Food(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now) # set the default value to current datetime
    food_name = models.CharField(max_length=255)
    calories_gained = models.FloatField()

    def __str__(self):
        return f"{self.user.username} - {self.food_name} - {self.date}"

