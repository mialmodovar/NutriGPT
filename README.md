# NutriGPT
NutriGPT is a natural language fitness application powered by OpenAI's GPT-4 language model. It assists users in tracking their daily calorie and nutrient intake through an intuitive conversational interface.

## Project Overview
This application employs a model with a single zero-shot prompt, providing a unique conversational interface where users can set goals, log meals, and track exercises. The app sends user's current stats and nutritional information to the model, which processes this data and generates appropriate conversational responses.

## Features
User Interaction and Data Handling
The app is designed to handle data communication between the user and the model seamlessly. The app communicates user's current stats and information, including their calorie goal, current calories, weight, height, age, gender, and current intake of protein, carbohydrates, and fats, to the model during the conversation. The model then uses this information to generate responses that are informative and engaging for the user.

### Goal Setting and Tracking
Users can set their protein, carbohydrate, fat, or calorie goals through a simple conversation with the model. When a user communicates their intake or an activity, such as eating a meal or performing an exercise, the app sends this information to the model. The model generates a response reflecting the food's calorie and macro count or the estimated calories burnt from the exercise. The app interprets these responses and updates the database accordingly, allowing users to effectively track their progress towards their goals.

### Undo Actions and Updates
In the event that a user wishes to undo a meal or an exercise action, the app communicates this to the model. The model generates a response that reflects the changes in intake and calories burnt. The app interprets this response and updates the database, providing users the flexibility to adjust their actions and maintain an accurate record of their intake and activities.

## Performance
The model boasts notable improvements over GPT-3.5 in terms of zero-shot performance. It handles longer prompts, has an enhanced ability to process nuanced instructions, and makes fewer factual errors. With a larger model size and a more extensive training dataset, the model demonstrates better contextual understanding and accuracy.

### Further Improvements
With the use of technologies like LangChain, GPT4All, and LLaMA, it's possible to create highly specialized chatbots, trained on substantial and specific datasets. These custom models can offer improved performance, particularly in specific domains like food values, where accuracy is crucial. LangChain's token-wise streaming and LLaMA's customization capabilities can create efficient natural language processing systems tailored to specific applications, thus enhancing the model's performance.

Furthermore, custom LLaMA models can be fine-tuned and enriched with embeddings for even more precise results. LangChain provides the ability to generate embeddings locally, improving data processing efficiency. Fine-tuning, albeit resource-intensive, allows a pre-trained model to incorporate new knowledge or adapt to a specific style, further improving the model's performance.

## Installation
### Clone the repository and navigate to the project directory.
<br>
### Set up a virtual environment for the project:
<br>
` bash ` <br>
` python -m venv myenv ` <br>
` source myenv/bin/activate `
<br>
### Install the project requirements: 
<br>
` pip install -r requirements.txt ` 
<br>
### Create a .env file inside the nutritiongpt/app directory with your OpenAI API key:
<br>
` OPEN_AI=YOUR_API_KEY_HERE `

