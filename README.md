# Weather Preparedness Application

A comprehensive weather preparedness application with an integrated chatbot that provides real-time weather data, forecasts, and safety tips for various weather conditions.

## Features

### Current Weather Information
- Real-time weather data from OpenWeatherMap API
- Temperature, humidity, wind speed, and conditions
- Location-based weather updates

### Weather Forecasts
- Multi-day weather forecasts
- Temperature trends and condition changes

### Interactive Chatbot
- Ask questions about weather safety for various conditions
  - Storms, hurricanes, tornadoes, floods, etc.
- Get real-time weather data for any city worldwide
- Receive personalized safety recommendations based on current conditions

### Emergency Preparedness
- Weather-specific safety guidelines
- Checklists for emergency kits
- Evacuation tips for severe weather events

## Getting Started

### Prerequisites
- Python 3.11 or higher
- OpenWeatherMap API key

### Installation

1. Clone this repository
2. Install required dependencies (flask, flask-cors, gunicorn, openai, requests, trafilatura)
3. Set up environment variables:
   - `OPENWEATHER_API_KEY`: Your OpenWeatherMap API key

### Running the Application

Start the application with:
```
python main.py
```
or use Gunicorn (recommended for production):
```
gunicorn --bind 0.0.0.0:5000 main:app
```

## Using the Chatbot

The chatbot can answer questions like:
- "What should I do during a hurricane?"
- "How do I prepare for a flood?"
- "What's the weather in London?"
- "Tell me about tornado safety"

The chatbot provides:
- Detailed safety instructions for specific weather conditions
- Current weather information for any city
- General emergency preparedness tips

## API Integration

This application uses the OpenWeatherMap API to retrieve weather data. You'll need to:
1. Register at [OpenWeatherMap](https://openweathermap.org/) to get an API key
2. Set your API key as an environment variable

## Project Structure

- `main.py`: Application entry point
- `app.py`: Flask application and route definitions
- `weather_api.py`: Weather API integration
- `chatbot.py`: Chatbot functionality and response generation
- `templates/`: HTML templates
- `static/`: CSS, JavaScript, and static assets

## License

This project is open source and available under the MIT License.

## Acknowledgements

- Weather data provided by [OpenWeatherMap](https://openweathermap.org/)
- Icons and imagery from various open source projects
what is the transformation techniques used to get responses