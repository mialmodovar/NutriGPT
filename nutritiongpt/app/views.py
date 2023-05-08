from django.shortcuts import render

from django.views.generic import TemplateView


from django.views.generic import TemplateView

import time

from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        # Add code here to get the response from GPT-4
        time.sleep(6)
        response = "Hello world"
        return JsonResponse({'response': response})
    return JsonResponse({'error': 'Invalid request method'})

@login_required
def index(request):
    return render(request, 'app/chat.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            time.sleep(3)
            auth_login(request, user)
            print('User created successfully!')
            return redirect('index') # Replace 'index' with the name of the view where you want to redirect after successful registration
        else:
            print('User creation failed!')
    else:
        form = UserCreationForm()
    return render(request, 'app/register.html', {'form': form})



def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('index') # Replace 'index' with the name of the view where you want to redirect after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})

@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')  # Replace 'login' with the name of the view where you want to redirect after logout
