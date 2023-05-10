# NutriGPT

NutriGPT is a web application that let's you keep track of your daily nutrition and exercise rates.

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

