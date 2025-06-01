import os
import logging
from flask import Flask, render_template, request, jsonify, session
from weather_api import get_weather_data, get_weather_alerts, get_forecast
from chatbot import get_chatbot_response
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
CORS(app)

# OpenWeatherMap API Key
OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY", "6314d6786d074e1195a9e6f69b973a67")
if not OPENWEATHER_API_KEY:
    logger.warning("OpenWeatherMap API key not set. Weather data may not be available.")

@app.route('/')
def index():
    """Render the main page of the weather app."""
    return render_template('index.html')

@app.route('/api/weather', methods=['GET'])
def weather():
    """API endpoint to get current weather data."""
    location = request.args.get('location', 'New York')
    try:
        weather_data = get_weather_data(location, api_key=OPENWEATHER_API_KEY)
        return jsonify(weather_data)
    except Exception as e:
        logger.error(f"Error fetching weather data: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/forecast', methods=['GET'])
def forecast():
    """API endpoint to get weather forecast."""
    location = request.args.get('location', 'New York')
    try:
        forecast_data = get_forecast(location, api_key=OPENWEATHER_API_KEY)
        return jsonify(forecast_data)
    except Exception as e:
        logger.error(f"Error fetching forecast data: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/alerts', methods=['GET'])
def alerts():
    """API endpoint to get weather alerts."""
    location = request.args.get('location', 'New York')
    try:
        alerts_data = get_weather_alerts(location, api_key=OPENWEATHER_API_KEY)
        return jsonify(alerts_data)
    except Exception as e:
        logger.error(f"Error fetching alerts data: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    """API endpoint for chatbot interactions."""
    try:
        # Log the received request
        logger.debug(f"Received chatbot request: {request.data}")
        
        # Parse the JSON data
        data = request.get_json()
        if data is None:
            logger.error("Failed to parse JSON data from request")
            return jsonify({"error": "Invalid JSON data"}), 400
            
        # Get the message from the data
        user_message = data.get('message', '')
        logger.debug(f"Extracted user message: '{user_message}'")
        
        # Get the chatbot response
        response = get_chatbot_response(user_message)
        logger.debug(f"Generated response: '{response}'")
        
        # Return the response
        return jsonify({"response": response})
    except Exception as e:
        logger.error(f"Error processing chatbot message: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return render_template('error.html', error="Page not found"), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors."""
    return render_template('error.html', error="Internal server error"), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
