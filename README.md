# Weather-Guardian
This is a web application that provides real-time weather data for any city worldwide. Along with current weather details like temperature, humidity, and conditions, it features an integrated chatbot that offers personalized advice based on the current weather—such as dressing suggestions, travel tips, and safety precautions. 
2. Objectives
The key objectives of this project are as follows:
•	To provide accurate real-time weather data from reliable sources.
•	Educate and inform users about emergency preparedness for various weather-related events.
•	To integrate a conversational AI chatbot for user-friendly access to safety guidelines.
•	To deliver personalized weather safety recommendations based on current conditions and user locations.
•	Support disaster risk reduction through timely information and action-oriented checklists.
________________________________________
3. Features of the Application
Current Weather Information
•	Live weather data are provided for any city using the OpenWeatherMap API.
•	Temperature, humidity, wind speed, and general weather conditions.
•	Supports location-based data retrieval for personalized updates.
Weather Forecasts
•	Offers multi-day forecasts with weather trends.
•	This includes temperature variation and condition predictions.
Interactive Chatbot
•	Answers user queries regarding safety during extreme weather events, such as storms, hurricanes, floods, and tornadoes.
•	Delivers real-time weather updates through natural language conversations.
•	Provides emergency preparedness advice tailored to current or forecasted weather conditions.
Emergency Preparedness
•	Contains safety checklists specific to different types of severe weather.
•	Provide evacuation tips, emergency kit recommendations, and precautionary measures.
•	Functions as a ready-reference tool for disaster readiness.
________________________________________
4. API Keys Used
•	OpenWeatherMap API Key:
The core of the application’s weather data was powered by OpenWeatherMap API. Developers are required to:
o	Register on OpenWeatherMap to obtain a unique API key.
o	The API key is set as an environmental variable (OPENWEATHER_API_KEY) to authenticate API requests.
________________________________________
5. Data, Process, and Methodology
Data Sources
•	OpenWeatherMap API: Provides up-to-date weather conditions and multiday forecasts.
•	User queries and chatbot inputs were processed to provide contextually relevant safety data and weather information.
Process Flow
1.	User Interaction: The user either views real-time weather updates or interacts with a chatbot.
2.	API Request: For weather-related queries, a request is sent to OpenWeatherMap using user input (e.g., city name).
3.	Response Handling:
o	The responses were parsed and displayed in the UI.
o	If a chatbot is used, it uses the weather context and built-in prompts to offer safety advice.
4.	Preparedness Guidance: Relevant safety checklists and tips are presented based on the detected weather events (storm, flood, etc.).
Methodology
•	Background: Developed in Python using Flask.
•	Chatbot Logic: Utilizes OpenAI for conversational capabilities.
•	APIs: REST API integration with OpenWeatherMap.
•	UI/UX: Responsive front-end for easy interaction and accessibility.
•	Deployment: Can be run using Flask directly or deployed with Gunicorn in production environments.
________________________________________
6. Results
The Weather Preparedness Application successfully achieved the goal of delivering a comprehensive weather awareness tool. Key outcomes include:
•	Timely and reliable weather updates for global locations.
•	Effective communication of emergency safety information through natural language.
•	Increased user awareness and preparedness for weather-related emergencies.
•	Scalable and modular systems that can be expanded with additional features or data sources.

