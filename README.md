# NutriGPT

NutriGPT is a web application built with Django that uses OpenAI's GPT-3.5 architecture to generate personalized nutrition plans for users based on their dietary preferences and goals.

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

The web application should now be accessible at http://127.0.0.1:8000/. 

Note: The above instructions assume that you have already obtained an API key from OpenAI. If you have not done so, please visit their website to learn more about their services and how to obtain an API key. 

## Usage

Once the web application is running, users can access the homepage to generate personalized nutrition plans. They will be prompted to enter information about their dietary preferences, goals, and any dietary restrictions they may have. NutriGPT will use this information to generate a personalized nutrition plan for the user, which they can then save, print, or email to themselves. 

Thank you for using NutriGPT!
