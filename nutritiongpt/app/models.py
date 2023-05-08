from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)  # in centimeters
    weight = models.FloatField(null=True, blank=True)  # in kilograms
    gender = models.CharField(max_length=10, choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")], null=True, blank=True)

    def __str__(self):
        return self.user.username

class DailyIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now) # set the default value to current date
    calories = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    carbohydrates = models.FloatField(default=0)
    fats = models.FloatField(default=0)

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user.username} - {self.date}"

@receiver(post_save, sender=User)
def create_user_profile_and_daily_intake(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        DailyIntake.objects.create(user=instance)