# NutriGPT

## Project Overview
This application uses GPT-4 with zero-shot prompts to assist users in tracking their daily calorie and nutrient intake. It provides a unique interface where users can set goals, log meals, and track exercises through natural language conversations.

## Features
Data Handling
The app receives user's current stats and info at the end of each prompt such as calorie goal, current calories, weight, height, age, gender, and current intake of protein, carbohydrates, and fats.

Setting Nutrient Goals
Users can set their protein, carbohydrate, or fat goal through a simple conversation. The app acknowledges the request and updates the database accordingly.

Setting Calorie Goal
Users can set their calorie goal in a similar fashion. The app acknowledges the request and updates the database.

Nutrient Tracking
The app is designed to be observant. When a user mentions what they've eaten, the app records the food along with its calorie and macro count.

Exercise Tracking
When a user mentions they've performed an exercise, the app records it and estimates the calories burnt.

Undoing Actions
The application allows users to undo meal and exercise actions, reflecting these changes in their intake and calories burnt.

## 
Performance
The application of GPT-4 in this project allowed for more accurate and reliable responses, and enhanced the overall user experience. The language model showed significant improvements in understanding complex zero-shot prompts as compared to its predecessor, GPT-3.5.

## Installation

1. Clone the repository and navigate to the project directory.

2. Set up a virtual environment for the project:
   ```
   python -m venv myenv
   source myenv/bin/activate
   ```

3. Install the project requirements:
   ```
   pip install -r requirements.txt
   ```

4. Create a .env file inside the `nutritiongpt/app` directory with your OpenAI API key:
   ```
   OPEN_AI=YOUR_API_KEY_HERE
   ```

5. Run the Django development server:
   ```
   python manage.py runserver
   ```


