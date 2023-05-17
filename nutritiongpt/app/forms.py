from django import forms
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    date_of_birth = forms.DateField(required=False)
    height = forms.FloatField(required=False)
    weight = forms.FloatField(required=False)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(), required=False)
    calories_goal = forms.FloatField(required=False)
    protein_goal = forms.FloatField(required=False)
    carbohydrates_goal = forms.FloatField(required=False)
    fats_goal = forms.FloatField(required=False)

    class Meta:
        model = UserProfile
        fields = ['date_of_birth', 'height', 'weight', 'gender', 'calories_goal', 'protein_goal', 'carbohydrates_goal', 'fats_goal']

class CustomUserChangeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']