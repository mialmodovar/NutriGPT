from django.shortcuts import render, redirect
from django.db.models.functions import Greatest
from django.views.generic import TemplateView

from django.utils import timezone
from django.views.generic import TemplateView

import time
from django.db.models import F
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from .models import UserProfile, DailyIntake, Exercise, Food
from .forms import UserProfileForm, CustomUserChangeForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import re
import os
from dotenv import load_dotenv
import openai
from django.core import serializers
load_dotenv()  # Load the .env file

gpt4_api_key = os.getenv('OPEN_AI')

@login_required
def chatbot_response(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        
        if len(message) < 10 or len(message) > 200:
            return JsonResponse({'response': "Please don't spam me"})
        # Initialize the OpenAI API with your API key
        openai.api_key = gpt4_api_key
        
        # Get the user's calorie goal and current calories
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        daily_intake, created = DailyIntake.objects.get_or_create(user=user, date=timezone.now())

        # Check if user has exceeded request limit
        if daily_intake.request_counter >= 15:
            return JsonResponse({'response': 'You have reached your maximum messages for the day'})

        # Calculate the user's age based on the date of birth
        age = timezone.now().year - user_profile.date_of_birth.year

        # Generate a response using GPT-4
        prompt = f"{message}\nCALORIE_GOAL: {user_profile.calories_goal}\nCURRENT_CALORIES: {daily_intake.calories}\nCURRENT_WEIGHT: {user_profile.weight}\nCURRENT_HEIGHT: {user_profile.height}\nAGE: {age}\nGENDER: {user_profile.gender}\nCURRENT_PROTEIN: {daily_intake.protein}\nCURRENT_CARBO: {daily_intake.carbohydrates}\nCURRENT_FATS: {daily_intake.fats}\nPROTEIN_GOAL: {user_profile.protein_goal}\nCARBO_GOAL: {user_profile.carbohydrates_goal}\nFATS_GOAL: {user_profile.fats_goal}"
        print(prompt)
        
        init = '''
Data Handling: You are a fitness companion for a fitness app interacting with users using natural language. You will receive the user's current stats and info at the end of each prompt: CALORIE GOAL: G, CURRENT CALORIES: C, CURRENT WEIGHT: W, CURRENT HEIGHT: H, AGE: A, GENDER: E, CURRENT_PROTEIN: P, CURRENT_CARBO: CB, CURRENT_FATS: F.

Setting Nutrient Goals: When a user requests to set their protein, carbo, or fat goal (e.g., "I want to set my protein goal to 100"), acknowledge the request with 'Your protein/carbo/fats goal has been set to L'. After a line break, print "UPDATE_DB", "UPDATED_PROTEIN_GOAL: L" or "UPDATED_CARBO_GOAL: L" or "UPDATED_FATS_GOAL: L".

Setting Calorie Goal: When a user requests to set their calorie goal (e.g., \\"I want to set my calorie goal to 2000\\"), acknowledge the request with 'Your calorie goal has been set to L'. After a line break, print "UPDATE_DB", "UPDATED_CALORIE_GOAL: L".

Nutrient Tracking: Be observant when the user mentions what they've eaten. If the user doesn't specify the quantity of food, assume one serving. Record the food and its calorie and macro count. After registering this, acknowledge to the user 'You've consumed Z with Y calories, P protein, C carbohydrates, and F fats'. Then print "UPDATE_DB", "FOOD_NAME: Z", "CALORIES_ADDED: Y", "PROTEIN_ADDED: P", "CARBO_ADDED: C", "FATS_ADDED: F" after a line break, where Y represents the calories of the eaten food, P the protein, C the carbohydrates, and F the fats.

Exercise Tracking: If a user mentions they've done some exercise, record that. After recording the exercise, acknowledge the user 'You've done X exercise which burnt Y calories'. Then print "UPDATE_DB", "EXERCISE_NAME: X" and "CALORIES_REMOVED: Y" after a line break, where X is the exercise performed and Y is the estimated calories burnt.

Undoing Actions: If the user undoes a meal, acknowledge them 'You've removed Y calories, P proteins, C carbs, and F fats from your intake'. Then print "UPDATE_DB", "CALORIES_REMOVED: Y", "PROTEIN_REMOVED: P", "CARBO_REMOVED: C", "FATS_REMOVED: F" where Y is the calorie count, P is the protein count, C is the carbs count and F is the fats count of the undone food. If the user undoes an exercise, acknowledge them 'You've added back Y calories that had been removed by X exercise'. Then print "UPDATE_DB", "CALORIES_ADDED: Y", after a line break, where Y is the calorie count and X is the exercise undone.

Meal Suggestions: When asked for meal suggestions to meet their daily calorie goal, calculate the remaining required calories (G-C=D) and suggest meals totaling approximately D calories. Acknowledge this with 'Here are some meals that could help you reach your calorie goal'.

Hidden Updates: The user should not see the updates mentioned in points 2, 3, 4, 5, and 6. Place these after a line break at the end of your responses, preceded by "UPDATE_DB".

Insights and Conversations: Maintain a conversational tone, providing brief insights (max 20 words) about healthy eating and lifestyle whenever the user shares information about their food intake or exercise. Keep the interaction as human-like as possible.

Scope of Interactions: Only respond to queries related to nutrition, healthy lifestyle, gym, exercising, yoga, self-care, and mental health. Ignore all other subjects.

Current Stats: Feel free to share the user's current stats, including their weight and height, when relevant to the conversation.

Python String Formatting: Ensure all responses are correctly formatted as Python strings, using line breaks ("\n") for proper formatting and readability.'''

        initprompt = f"{init}"
        # Prepare the messages for the API call
        messages = [
            {"role": "system", "content": initprompt},
            {"role": "assistant", "content": "OK."},
        ]

        # If the conversation history is not None, append the last user prompt and response
        if user_profile.conversation is not None:
            messages.append({"role": "user", "content": user_profile.conversation["prompt"]})
            messages.append({"role": "assistant", "content": user_profile.conversation["response"]})

        # Add the current prompt
        messages.append({"role": "user", "content": prompt})

        response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=messages,
        max_tokens=800,
        temperature = 0.6
        )   

        # Extract the first response generated by GPT-4
        bot_response = response['choices'][0]['message']['content'].strip()

        # Increment the request counter and save the conversation history
        daily_intake.request_counter += 1
        daily_intake.save()
        user_profile.conversation = {"prompt": message, "response": bot_response}
        user_profile.save()

        # Rest of your code follows...


        # Check if "UPDATE_DB" is in the response
        if "UPDATE_DB" in bot_response:
            bot_response, db_update = bot_response.split("UPDATE_DB", 1)
        else:
            db_update = None
        print(db_update)

        update_dict = {}
        if db_update:
            update_strings = ["UPDATED_CALORIE_GOAL", "CALORIES_ADDED", "CALORIES_REMOVED", "PROTEIN_ADDED", "CARBO_ADDED", "FATS_ADDED", "FOOD_NAME", "EXERCISE_NAME", "PROTEIN_REMOVED", "CARBO_REMOVED", "FATS_REMOVED", "UPDATED_PROTEIN_GOAL", "UPDATED_CARBO_GOAL", "UPDATED_FATS_GOAL"]
            for string in update_strings:
                if string in db_update:
                    if string in ["FOOD_NAME", "EXERCISE_NAME"]:
                        # Extract the string after the string (and colon)
                        match = re.search(f"{string}: ([\w\s]+)", db_update)
                        if match:
                                text = match.group(1).strip()
                                # Remove everything after \n
                                text = text.split('\n')[0]
                                # Store the value in the dictionary
                                update_dict[string] = text
                    else:
                        # Extract the number after the string (and colon)
                        match = re.search(f"{string}: ([\d\.]+)", db_update)
                        if match:
                            number = float(match.group(1).strip())
                            # Store the value in the dictionary
                            update_dict[string] = number

        print(update_dict)

        if "PROTEIN_REMOVED" in update_dict:
            daily_intake.protein = Greatest(F('protein') - update_dict["PROTEIN_REMOVED"], 0)
            daily_intake.save()
            daily_intake.refresh_from_db() 

        if "CARBO_REMOVED" in update_dict:
            daily_intake.carbohydrates = Greatest(F('carbohydrates') - update_dict["CARBO_REMOVED"], 0)
            daily_intake.save()
            daily_intake.refresh_from_db() 

        if "FATS_REMOVED" in update_dict:
            daily_intake.fats = Greatest(F('fats') - update_dict["FATS_REMOVED"], 0)
            daily_intake.save()
            daily_intake.refresh_from_db() 

        if "UPDATED_PROTEIN_GOAL" in update_dict:
            user_profile.protein_goal = update_dict["UPDATED_PROTEIN_GOAL"]
            user_profile.save()
            user_profile.refresh_from_db() 

        if "UPDATED_CARBO_GOAL" in update_dict:
            user_profile.carbohydrates_goal = update_dict["UPDATED_CARBO_GOAL"]
            user_profile.save()
            user_profile.refresh_from_db() 

        if "UPDATED_FATS_GOAL" in update_dict:
            user_profile.fats_goal = update_dict["UPDATED_FATS_GOAL"]
            user_profile.save()
            user_profile.refresh_from_db() 
        
        if "UPDATED_CALORIE_GOAL" in update_dict:
            user_profile.calories_goal = update_dict["UPDATED_CALORIE_GOAL"]
            user_profile.save()
            user_profile.refresh_from_db() 

        if "CALORIES_ADDED" in update_dict:
            daily_intake.calories = F('calories') + update_dict["CALORIES_ADDED"]
            daily_intake.save()
            daily_intake.refresh_from_db() 

        if "CALORIES_REMOVED" in update_dict:
            daily_intake.calories = F('calories') - update_dict.get("CALORIES_REMOVED", 0) 
            daily_intake.save()
            daily_intake.refresh_from_db() 

        if "PROTEIN_ADDED" in update_dict:
            daily_intake.protein = F('protein') + update_dict["PROTEIN_ADDED"]
            daily_intake.save()
            daily_intake.refresh_from_db() 

        if "CARBO_ADDED" in update_dict:
            daily_intake.carbohydrates = F('carbohydrates') + update_dict["CARBO_ADDED"]
            daily_intake.save()
            daily_intake.refresh_from_db() 

        if "FATS_ADDED" in update_dict:
            daily_intake.fats = F('fats') + update_dict["FATS_ADDED"]
            daily_intake.save()
            daily_intake.refresh_from_db() 

        if "FOOD_NAME" in update_dict:
            food = Food.objects.create(user=user, date=timezone.now(), food_name=update_dict["FOOD_NAME"], calories_gained=update_dict.get("CALORIES_ADDED", 0))

        if "EXERCISE_NAME" in update_dict:
            exercise = Exercise.objects.create(user=user, date=timezone.now(), exercise_name=update_dict["EXERCISE_NAME"], calories_burned=update_dict.get("CALORIES_REMOVED", 0))

        print(bot_response)
        bot_response = f"{bot_response}"
        bot_response = bot_response.replace('\n', '<br>')
        print(bot_response)
        return JsonResponse({'response': bot_response})

       
    
    return JsonResponse({'error': 'Invalid request method'})

@login_required
def chat(request):
    daily_intake, created = DailyIntake.objects.get_or_create(user=request.user, date=timezone.now())
    return render(request, 'app/chat.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Create UserProfile instance
            user_profile = UserProfile(user=user)
            user_profile.save()

            # Create DailyIntake instance
            daily_intake = DailyIntake(user=user, date=timezone.now())
            daily_intake.save()

            time.sleep(3)
            auth_login(request, user)
            print('User created successfully!')
            return redirect('dashboard') # Replace 'index' with the name of the view where you want to redirect after successful registration
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
            return redirect('dashboard') # Replace 'index' with the name of the view where you want to redirect after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})


@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')  # Replace 'login' with the name of the view where you want to redirect after logout

@login_required
def edit_profile(request):
    if request.method == 'POST':
        print('dod')
        profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if profile_form.is_valid():
            print('valid')
            profile_form.save()
            # Add a success message or redirect
        else:
            print('fods')
            print(profile_form.errors)
    else:
        profile_form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'app/editprofile.html', {'profile_form': profile_form})

def food_diary(request):
    # Get the current user
    user = request.user

    # Get all Food objects for the current user
    foods = Food.objects.filter(user=user)

    # Render the template with the foods context
    return render(request, 'app/food_intake.html', {'foods': foods})

def exercise_diary(request):
    # Get the current user
    user = request.user

    # Get all Food objects for the current user
    exercises = Exercise.objects.filter(user=user)

    # Render the template with the foods context
    return render(request, 'app/exercise_diary.html', {'exercises': exercises})


@login_required
def dashboard(request):
    daily_intake, created = DailyIntake.objects.get_or_create(user=request.user, date=timezone.now())
    return render(request, 'app/dashboard.html')



@login_required
def get_dashboard_data(request):
    user = request.user
    daily_intake = DailyIntake.objects.get(user=user, date=timezone.now().date())
    userprofile = UserProfile.objects.get(user=user)

    calories_percentage = int(min(daily_intake.calories / userprofile.calories_goal * 100, 100))
    protein_percentage = int(min(daily_intake.protein / userprofile.protein_goal * 100, 100))
    carbs_percentage = int(min(daily_intake.carbohydrates / userprofile.carbohydrates_goal * 100, 100))
    fats_percentage = int(min(daily_intake.fats / userprofile.fats_goal * 100, 100))

    exercises = Exercise.objects.filter(user=user, date=timezone.now().date())

    foods = Food.objects.filter(user=user, date=timezone.now().date())

    return JsonResponse({
        'daily_intake': {
            'calories': daily_intake.calories,
            'protein': daily_intake.protein,
            'carbohydrates': daily_intake.carbohydrates,
            'fats': daily_intake.fats,
        },
        'userprofile': {
            'calories_goal': userprofile.calories_goal,
            'protein_goal': userprofile.protein_goal,
            'carbohydrates_goal': userprofile.carbohydrates_goal,
            'fats_goal': userprofile.fats_goal,
        },
        'calories_percentage': calories_percentage,
        'protein_percentage': protein_percentage,
        'carbs_percentage': carbs_percentage,
        'fats_percentage': fats_percentage,
        'exercises': serializers.serialize('json', exercises),
        'foods': serializers.serialize('json', foods)

    })