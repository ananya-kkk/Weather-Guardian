import requests
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_weather_data(location, api_key):
    """
    Fetches current weather data from OpenWeatherMap API.
    
    Args:
        location (str): The city name or coordinates.
        api_key (str): OpenWeatherMap API key.
        
    Returns:
        dict: Weather data including temperature, humidity, etc.
    """
    if not api_key:
        raise ValueError("OpenWeatherMap API key is required")
    
    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': location,
        'appid': api_key,
        'units': 'metric'  # Use metric units (Celsius)
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an exception for HTTP errors
        
        data = response.json()
        logger.debug(f"Weather data fetched successfully for {location}")
        
        # Format the response data
        weather_data = {
            'location': data['name'],
            'country': data['sys']['country'],
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
            'timestamp': datetime.now().isoformat(),
            'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'),
            'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')
        }
        
        return weather_data
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching weather data: {str(e)}")
        raise Exception(f"Failed to fetch weather data: {str(e)}")

def get_forecast(location, api_key, days=5):
    """
    Fetches weather forecast from OpenWeatherMap API.
    
    Args:
        location (str): The city name or coordinates.
        api_key (str): OpenWeatherMap API key.
        days (int): Number of days for forecast.
        
    Returns:
        dict: Weather forecast data.
    """
    if not api_key:
        raise ValueError("OpenWeatherMap API key is required")
    
    url = f"https://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': location,
        'appid': api_key,
        'units': 'metric'  # Use metric units (Celsius)
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        logger.debug(f"Forecast data fetched successfully for {location}")
        
        # Format the forecast data (every 8th entry is approximately a day)
        forecast_data = []
        for i, forecast in enumerate(data['list']):
            if i % 8 == 0 and len(forecast_data) < days:  # Get one entry per day
                forecast_item = {
                    'date': datetime.fromtimestamp(forecast['dt']).strftime('%Y-%m-%d'),
                    'day': datetime.fromtimestamp(forecast['dt']).strftime('%A'),
                    'temperature': forecast['main']['temp'],
                    'feels_like': forecast['main']['feels_like'],
                    'humidity': forecast['main']['humidity'],
                    'description': forecast['weather'][0]['description'],
                    'icon': forecast['weather'][0]['icon']
                }
                forecast_data.append(forecast_item)
        
        return {
            'location': data['city']['name'],
            'country': data['city']['country'],
            'forecast': forecast_data
        }
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching forecast data: {str(e)}")
        raise Exception(f"Failed to fetch forecast data: {str(e)}")

def get_weather_alerts(location, api_key):
    """
    Fetches weather alerts from OpenWeatherMap API.
    
    Args:
        location (str): The city name or coordinates.
        api_key (str): OpenWeatherMap API key.
        
    Returns:
        dict: Weather alerts data.
    """
    if not api_key:
        raise ValueError("OpenWeatherMap API key is required")
    
    # First, get the coordinates from the location
    try:
        geo_url = f"https://api.openweathermap.org/geo/1.0/direct"
        geo_params = {
            'q': location,
            'limit': 1,
            'appid': api_key
        }
        
        geo_response = requests.get(geo_url, params=geo_params)
        geo_response.raise_for_status()
        
        geo_data = geo_response.json()
        if not geo_data:
            return {"location": location, "alerts": [], "has_alerts": False, "message": "No location found"}
        
        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']
        
        # Try to use the One Call API (which requires paid subscription)
        try:
            url = f"https://api.openweathermap.org/data/2.5/onecall"
            params = {
                'lat': lat,
                'lon': lon,
                'exclude': 'minutely,hourly',
                'appid': api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            logger.debug(f"Weather alerts fetched successfully for {location}")
            
            # Extract alerts if available
            alerts = []
            if 'alerts' in data:
                for alert in data['alerts']:
                    alert_item = {
                        'event': alert.get('event', 'Unknown event'),
                        'description': alert.get('description', 'No description available'),
                        'start': datetime.fromtimestamp(alert.get('start', 0)).isoformat(),
                        'end': datetime.fromtimestamp(alert.get('end', 0)).isoformat(),
                        'sender': alert.get('sender_name', 'Unknown source')
                    }
                    alerts.append(alert_item)
            
            return {
                'location': location,
                'alerts': alerts,
                'has_alerts': len(alerts) > 0
            }
            
        except requests.exceptions.HTTPError as e:
            # Handle 401 Unauthorized (free tier doesn't have access to One Call API)
            if e.response.status_code == 401:
                logger.warning(f"One Call API access not available (requires paid subscription): {str(e)}")
                return {
                    'location': location,
                    'alerts': [],
                    'has_alerts': False,
                    'subscription_required': True,
                    'message': "Weather alerts require OpenWeather paid subscription"
                }
            else:
                raise
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching weather alerts: {str(e)}")
        raise Exception(f"Failed to fetch weather alerts: {str(e)}")
