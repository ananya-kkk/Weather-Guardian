import re
import random
import logging
from datetime import datetime
import os
from weather_api import get_weather_data

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Get OpenWeatherMap API key
OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY", "6314d6786d074e1195a9e6f69b973a67")

# Enhanced dictionary of weather-related keywords and responses
WEATHER_RESPONSES = {
    'rain': [
        "During rain, it's important to:\n• Carry an umbrella or wear a waterproof raincoat\n• Drive cautiously as roads become slippery\n• Avoid flooded areas - just 6 inches of water can sweep you off your feet\n• Ensure proper drainage around your home to prevent water damage\n• Stay indoors during thunderstorms and lightning",
        "Rainy conditions require these safety measures:\n• Use headlights while driving to improve visibility\n• Avoid driving through flooded areas - water can damage your engine\n• Be cautious of hydroplaning by reducing speed\n• Have proper rain gear if you need to go outside\n• Check weather alerts for flash flood warnings",
        "When it's raining, remember to:\n• Keep electronic devices away from water\n• Watch for lightning and seek shelter if thunderstorms develop\n• Allow extra time for travel and commuting\n• Have a backup plan for outdoor activities\n• Monitor local weather updates for changing conditions"
    ],
    'snow': [
        "In snowy conditions, your safety depends on:\n• Dressing in warm, waterproof layers and proper footwear\n• Driving slowly with increased following distance\n• Keeping emergency supplies in your vehicle (blankets, food, water)\n• Clearing snow from walkways and driveways to prevent falls\n• Checking on elderly neighbors who may need assistance",
        "When snow is in the forecast:\n• Prepare your home by insulating pipes to prevent freezing\n• Stock up on essentials before the storm arrives\n• Plan for potential power outages with alternative heat sources\n• Use snow tires or chains when driving is necessary\n• Remove snow from roofs if accumulation becomes heavy",
        "Snow safety tips include:\n• Avoiding overexertion when shoveling - take breaks and stay hydrated\n• Being aware of signs of hypothermia and frostbite\n• Keeping your cell phone charged in case of emergency\n• Having alternative communication methods if power fails\n• Staying updated on road closures and travel advisories"
    ],
    'storm': [
        "During a storm, protect yourself by:\n• Staying indoors and away from windows\n• Securing outdoor objects that could become projectiles\n• Having emergency supplies ready (flashlights, batteries, radio)\n• Unplugging electronic devices to prevent damage from lightning\n• Moving to an interior room on the lowest floor if severe",
        "Storm safety is critical - remember to:\n• Create a family communication plan before storms arrive\n• Know the difference between watches (possible) and warnings (imminent)\n• Keep trees trimmed to prevent damage from falling branches\n• Have multiple ways to receive weather alerts\n• Prepare for power outages with backup charging options",
        "When storms threaten, take these precautions:\n• Fill bathtubs with water for sanitation needs if water service is interrupted\n• Keep important documents in waterproof containers\n• Have a plan for pets and livestock\n• Know evacuation routes if you live in a flood-prone area\n• Avoid using landline phones during lightning storms"
    ],
    'hurricane': [
        "Hurricane preparedness includes:\n• Creating a comprehensive evacuation plan and following official orders\n• Securing your home - board up windows and reinforce doors\n• Assembling an emergency kit with 3-7 days of supplies\n• Keeping important documents in waterproof containers\n• Having cash on hand as ATMs may not work during power outages",
        "Before a hurricane arrives:\n• Know your evacuation zone and have multiple route options\n• Clear gutters and drains to prevent water damage\n• Fill your vehicle's gas tank and prepare backup transportation\n• Store outdoor furniture and other items that could become projectiles\n• Have medication supplies for at least two weeks",
        "Hurricane safety requires:\n• Understanding the dangers of storm surge - the deadliest hurricane hazard\n• Never ignoring evacuation orders from local authorities\n• Maintaining multiple communication methods\n• Preparing for extended power and water outages\n• Having a plan for family members with special needs"
    ],
    'tornado': [
        "During a tornado warning:\n• Seek shelter immediately in a basement or interior room on the lowest floor\n• Stay away from windows and cover yourself with blankets or a mattress\n• Put on sturdy shoes and helmet for head protection\n• Keep a whistle to signal for help if trapped\n• If in a vehicle, never try to outrun a tornado - seek sturdy shelter",
        "Tornado safety depends on quick action:\n• Know the warning signs: dark/greenish sky, large hail, loud roar\n• Practice tornado drills with your family regularly\n• Identify safe rooms in advance - interior rooms with no windows\n• Have weather alert radios with battery backup\n• After a tornado, watch for downed power lines and gas leaks",
        "If a tornado threatens:\n• Mobile homes provide little protection - seek sturdier shelter\n• If caught outside with no shelter, lie flat in a ditch away from vehicles\n• Never shelter under an overpass - wind speeds increase in these areas\n• Keep emergency supplies in your designated shelter area\n• Have a plan for reuniting with family members"
    ],
    'heat': [
        "During extreme heat:\n• Stay hydrated by drinking plenty of water, even if not thirsty\n• Avoid outdoor activities during peak heat (10am-4pm)\n• Wear lightweight, light-colored, loose-fitting clothing\n• Use air conditioning or spend time in public cooled places\n• Check on elderly neighbors and those with health conditions",
        "Heat safety is essential:\n• Never leave children or pets in vehicles, even briefly\n• Take cool showers or baths to lower body temperature\n• Use fans with open windows to create cross-ventilation\n• Recognize heat illness symptoms: headache, dizziness, nausea\n• Limit strenuous activities and take frequent breaks in shade",
        "Protecting yourself in hot weather means:\n• Eating lighter meals that don't require cooking\n• Avoiding alcohol and caffeine which can cause dehydration\n• Applying sunscreen (SPF 15+) and reapplying every 2 hours\n• Wearing a wide-brimmed hat and sunglasses outdoors\n• Knowing the difference between heat exhaustion and heat stroke"
    ],
    'cold': [
        "In extreme cold conditions:\n• Dress in layers with moisture-wicking inner layers\n• Keep head, hands, feet, and face well protected\n• Limit time outdoors and watch for signs of hypothermia and frostbite\n• Maintain emergency supplies in your home and vehicle\n• Check heating systems and carbon monoxide detectors",
        "Cold weather safety requires:\n• Understanding wind chill factor which accelerates heat loss\n• Avoiding alcohol which gives a false sense of warmth\n• Keeping moving to generate body heat when outdoors\n• Preparing for winter travel with emergency car kits\n• Having alternative heating methods in case of power failure",
        "When temperatures drop dangerously low:\n• Know the symptoms of hypothermia: shivering, confusion, drowsiness\n• Recognize frostbite signs: numbness, white/grayish skin, firm/waxy feel\n• Keep pets indoors or provide adequate shelter\n• Prevent frozen pipes by maintaining heat and allowing faucets to drip\n• Check on elderly or disabled neighbors who may need assistance"
    ],
    'flood': [
        "During flooding events:\n• Never walk or drive through floodwaters - 6 inches of moving water can knock you down\n• Move to higher ground and avoid bridges over fast-moving water\n• Disconnect utilities if instructed and avoid electrical equipment if wet\n• Prepare an emergency kit and know evacuation routes\n• After floods, be aware of contaminated water and damaged roadways",
        "Flood safety measures include:\n• Elevating electrical systems and waterproofing basements if in flood-prone areas\n• Having flood insurance even if not in a high-risk zone\n• Keeping important documents in waterproof containers\n• Following evacuation orders immediately\n• Avoiding contact with floodwater which may contain sewage and chemicals",
        "When flooding threatens:\n• Know the difference between flood watch (possible) and warning (occurring)\n• Have multiple ways to receive emergency alerts\n• Plan for pets and livestock evacuation\n• Practice your evacuation route before flooding occurs\n• After flooding, document damage for insurance and be aware of mold risks"
    ],
    'earthquake': [
        "During an earthquake:\n• Drop, cover, and hold on - get under sturdy furniture\n• Stay away from windows, exterior walls, and heavy objects that could fall\n• If in bed, stay there and protect your head with a pillow\n• If outdoors, move to an open area away from buildings and utility wires\n• After shaking stops, be prepared for aftershocks",
        "Earthquake preparedness includes:\n• Securing heavy furniture, appliances, and hanging objects\n• Identifying safe spots in each room (under sturdy tables, against interior walls)\n• Having emergency supplies accessible\n• Knowing how to shut off gas, water, and electricity\n• Creating a family communication plan with meeting places",
        "After an earthquake:\n• Check yourself and others for injuries before moving\n• Evacuate if your building is damaged or if you smell gas\n• Avoid using elevators or damaged staircases\n• Be cautious of fallen power lines and broken gas lines\n• Monitor local news for emergency information and instructions"
    ],
    'wildfire': [
        "If wildfires threaten your area:\n• Be ready to evacuate at a moment's notice - have go-bags prepared\n• Create defensible space around your home by clearing vegetation\n• Close all windows, vents, and doors to prevent embers from entering\n• Move flammable furniture away from exterior walls\n• Follow evacuation routes provided by local authorities",
        "Wildfire safety requires preparation:\n• Maintain an emergency supply kit ready to go\n• Have a family communication plan with meeting locations\n• Register for emergency alert systems in your area\n• Keep important documents in fire-resistant containers\n• Know multiple evacuation routes from your neighborhood",
        "During wildfire season:\n• Stay informed about fire conditions and air quality\n• Keep your vehicle fueled and ready for quick evacuation\n• Wear proper clothing if near smoke: long sleeves, pants, N95 masks\n• Follow all fire restrictions and bans in your area\n• After fires, be aware of flash flood risks in burn scar areas"
    ]
}

# Enhanced general weather preparedness tips
GENERAL_TIPS = [
    "Creating a comprehensive emergency preparedness plan involves:\n• Assembling an emergency kit with water (1 gallon per person per day)\n• Stocking non-perishable food, medications, and first aid supplies\n• Including battery-powered radio, flashlights, and extra batteries\n• Having cash in small denominations and copies of important documents\n• Planning for specific needs of family members, pets, and the elderly",
    
    "Family emergency planning should include:\n• Establishing meeting places both in your neighborhood and outside the area\n• Identifying an out-of-area contact everyone can communicate through\n• Practicing evacuation routes and shelter locations\n• Knowing how to shut off utilities at your home\n• Creating emergency contact cards for each family member",
    
    "Stay informed during emergencies by:\n• Having multiple information sources (NOAA weather radio, mobile alerts)\n• Following local emergency management agencies on social media\n• Downloading emergency apps from FEMA, Red Cross, and local agencies\n• Understanding warning systems in your community\n• Keeping backup power sources for communication devices",
    
    "Critical documents for emergency preparedness:\n• Store in waterproof, portable containers: insurance policies, identification\n• Include medical information, property records and financial documents\n• Consider cloud storage backup for digital copies\n• Have emergency contact lists for family, neighbors, and important services\n• Include maps of your area with evacuation routes marked",
    
    "Building emergency resilience means:\n• Learning basic life-saving skills like CPR and first aid\n• Knowing how to operate fire extinguishers and when to use them\n• Understanding how to purify water if supplies are contaminated\n• Being able to safely use backup heating and power sources\n• Creating emergency plans for different scenarios (home fires, natural disasters)"
]

# Enhanced greetings and farewell responses
GREETINGS = [
    "Hello! I'm your Weather Preparedness Assistant. I provide current weather data, safety tips, travel recommendations, and alternative action suggestions based on conditions in your area. How can I help you stay safe today?",
    
    "Hi there! I'm your Weather Safety Assistant. Ask me about weather conditions in any city, and I'll give you detailed safety information, travel advisories, and recommended actions based on current conditions. What would you like to know?",
    
    "Welcome to the Weather Preparedness Assistant! I can assess weather safety, provide travel recommendations, and suggest appropriate actions for any location. Try asking 'Is it safe to travel in [city]?' or 'What's the weather in [city]?'"
]

FAREWELLS = [
    "Stay safe and weather-aware! Remember to check forecasts regularly and have your emergency plans updated. Feel free to ask if you have more questions in the future.",
    
    "Thanks for chatting! I'm always here to help with weather safety information and updates. Remember that preparedness is key to staying safe in any weather condition.",
    
    "I hope that information helps keep you safe! Weather can change quickly, so stay informed through multiple alert systems. Come back anytime for more weather safety guidance."
]

# Enhanced unknown response fallbacks
UNKNOWN_RESPONSES = [
    "I'm not sure I understood your question. I can provide weather safety information, travel recommendations, and alternative action suggestions for any location. Try asking 'Is it safe to travel in [city]?' or 'What's the weather in [city]?'",
    
    "I didn't quite catch that. For best results, ask me about weather conditions and travel safety in specific locations. I can tell you if it's safe to travel and what precautions to take based on current weather conditions.",
    
    "I'm designed to provide weather-based safety recommendations. Try asking something like 'Should I drive in Chicago today?' or 'What's the weather in Miami?' to get detailed safety tips, travel advisories, and suggested actions."
]

def get_city_from_text(text):
    """
    Extract a city name from the text using common patterns for weather and travel queries.
    Filters out time-related words to avoid API errors.
    """
    # Log the original text
    logger.debug(f"Extracting city from: {text}")
    
    # Enhanced patterns to handle both weather and travel queries
    city_patterns = [
        # Weather patterns
        r'weather\s+in\s+([A-Za-z]+(?:\s+[A-Za-z]+)*)',
        r'what(?:\'s|\s+is)\s+(?:the\s+)?weather\s+in\s+([A-Za-z]+(?:\s+[A-Za-z]+)*)',
        r'how\s+is\s+(?:the\s+)?weather\s+in\s+([A-Za-z]+(?:\s+[A-Za-z]+)*)',
        r'([A-Za-z]+(?:\s+[A-Za-z]+)*)\s+weather',
        
        # Travel safety patterns
        r'(?:travel|drive|driving|commute)\s+(?:to|in|through|around|near)\s+([A-Za-z]+(?:\s+[A-Za-z]+)*)',
        r'(?:safe|safety|conditions)\s+(?:to|in|for)\s+(?:travel|drive|commute|go)\s+(?:to|in|through|around|near)\s+([A-Za-z]+(?:\s+[A-Za-z]+)*)',
        r'(?:safe|safety|conditions)\s+(?:in|for|of|at)\s+([A-Za-z]+(?:\s+[A-Za-z]+)*)',
        
        # Road/route patterns
        r'(?:road|route|traffic|highway)\s+(?:condition|status)\s+(?:in|to|near|around)\s+([A-Za-z]+(?:\s+[A-Za-z]+)*)',
        
        # General location patterns (must be last to avoid false positives)
        r'(?:in|at|to|from|near)\s+([A-Za-z]+(?:\s+[A-Za-z]+)*)'
    ]
    
    # Words to be excluded from city names - these common words, time references
    # and modal words should not be part of the city name
    excluded_words = [
        # Common words
        'the', 'there', 'here', 'this', 'that', 'these', 'those', 'outside', 'inside', 
        'general', 'currently', 'presently', 'such', 'going', 'like', 'have', 'has',
        # Time references that often appear in queries
        'today', 'tomorrow', 'yesterday', 'morning', 'afternoon', 'evening', 'night', 
        'now', 'later', 'current', 'present', 'soon', 'moment', 'future', 'past',
        # Modal verbs and question words
        'should', 'would', 'could', 'can', 'may', 'might', 'must', 'shall', 'will',
        'who', 'what', 'when', 'where', 'why', 'how'
    ]
    
    # Use original case-preserving text for extraction
    for pattern in city_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            # Get the potential city name
            raw_city = match.group(1).strip()
            
            # Skip if the entire extracted text is in our excluded words list
            if raw_city.lower() in excluded_words:
                continue
            
            # Split the city name into words
            city_words = raw_city.split()
            
            # Filter out excluded words from the city name
            filtered_city_words = [word for word in city_words if word.lower() not in excluded_words]
            
            # If we have no words left after filtering, continue to next pattern
            if not filtered_city_words:
                continue
                
            # Reconstruct the city name
            city = " ".join(filtered_city_words)
            
            logger.debug(f"Extracted and filtered city: {city}")
            return city
    
    return None

def format_weather_response(data):
    """
    Format weather data into a readable response with safety recommendations.
    
    Provides:
    1. Current weather summary
    2. Safety tips relevant to weather conditions
    3. Travel safety recommendation
    4. Alternative action suggestions
    """
    if 'error' in data:
        return f"Sorry, I couldn't get weather information: {data['error']}"
    
    try:
        # 1. Brief summary of the current weather
        response = f"📍 **Weather in {data['location']}, {data['country']}**\n\n"
        response += f"🌡️ Current temperature: {int(round(data['temperature']))}°C (feels like {int(round(data['feels_like']))}°C)\n"
        response += f"💧 Humidity: {data['humidity']}%\n"
        response += f"💨 Wind: {data['wind_speed']} m/s\n"
        response += f"☁️ Conditions: {data['description'].capitalize()}\n\n"
        
        # Extract weather conditions
        description = data['description'].lower()
        temp = data['temperature']
        wind_speed = data['wind_speed']
        
        # Determine weather condition category
        weather_condition = "normal"
        is_travel_safe = True
        travel_warning = ""
        safety_tips = []
        alternative_actions = []
        
        # 2. Determine condition and safety tips
        if 'rain' in description or 'drizzle' in description or 'shower' in description:
            weather_condition = "rain"
            safety_tips = [
                "Use caution while driving as roads may be slippery",
                "Carry an umbrella or raincoat if going outside",
                "Watch for potential flooding in low-lying areas"
            ]
            
            if 'heavy' in description or 'thunderstorm' in description:
                is_travel_safe = False
                travel_warning = "Heavy rain reduces visibility and increases risk of hydroplaning."
                alternative_actions = [
                    "Consider delaying non-essential travel until conditions improve",
                    "Work from home if possible",
                    "If you must drive, reduce speed significantly and turn on headlights"
                ]
            else:
                alternative_actions = [
                    "Allow extra travel time",
                    "Ensure your vehicle's wipers and lights are working properly",
                    "Check for road closures before departing"
                ]
                
        elif 'snow' in description or 'blizzard' in description:
            weather_condition = "snow"
            safety_tips = [
                "Dress warmly in layers when going outside",
                "Drive cautiously and maintain safe distances",
                "Clear walkways to prevent slips and falls"
            ]
            
            if 'blizzard' in description or 'heavy' in description:
                is_travel_safe = False
                travel_warning = "Heavy snow creates hazardous road conditions and poor visibility."
                alternative_actions = [
                    "Stay home if possible and avoid all unnecessary travel",
                    "Work remotely if your job allows it",
                    "Stock up on essentials before the snow intensifies"
                ]
            else:
                alternative_actions = [
                    "Use public transportation instead of driving if available",
                    "Ensure your vehicle has appropriate snow tires or chains",
                    "Carry emergency supplies if travel is necessary"
                ]
                
        elif 'storm' in description or 'thunder' in description:
            weather_condition = "storm"
            safety_tips = [
                "Stay indoors and away from windows",
                "Unplug sensitive electronics",
                "Have emergency supplies ready in case of power outages"
            ]
            
            is_travel_safe = False
            travel_warning = "Thunderstorms present dangers from lightning, high winds, and possible flooding."
            alternative_actions = [
                "Postpone all non-emergency travel",
                "If caught outside, avoid tall objects and open areas",
                "Keep devices charged in case of power outages"
            ]
                
        elif 'fog' in description or 'mist' in description:
            weather_condition = "fog"
            safety_tips = [
                "Use low-beam headlights when driving",
                "Reduce speed and increase following distance",
                "Allow extra time for travel"
            ]
            
            if 'dense' in description or 'thick' in description:
                is_travel_safe = False
                travel_warning = "Dense fog severely limits visibility making all forms of travel hazardous."
                alternative_actions = [
                    "Delay travel until fog clears if possible",
                    "Consider alternative routes avoiding high-speed roads",
                    "If you must drive, use fog lights and proceed with extreme caution"
                ]
            else:
                alternative_actions = [
                    "Plan for longer travel times",
                    "Consider delaying travel if visibility is poor",
                    "Stay informed about changing visibility conditions"
                ]
                
        elif temp > 35:
            weather_condition = "extreme heat"
            safety_tips = [
                "Stay hydrated by drinking plenty of water",
                "Seek air-conditioned environments",
                "Avoid strenuous outdoor activities"
            ]
            
            is_travel_safe = False
            travel_warning = "Extreme heat can cause vehicle overheating and heat-related illness."
            alternative_actions = [
                "Postpone outdoor activities to cooler parts of the day",
                "Check on elderly or vulnerable individuals",
                "Carry extra water if travel is necessary"
            ]
                
        elif temp > 30:
            weather_condition = "heat"
            safety_tips = [
                "Stay hydrated by drinking plenty of water",
                "Seek shade and limit outdoor activities during peak hours",
                "Check on vulnerable individuals who may be heat-sensitive"
            ]
            
            alternative_actions = [
                "Plan outdoor activities for early morning or evening",
                "Wear lightweight, light-colored clothing",
                "Use sunscreen and wear a hat when outdoors"
            ]
                
        elif temp < -10:
            weather_condition = "extreme cold"
            safety_tips = [
                "Limit exposure to prevent frostbite and hypothermia",
                "Dress in multiple warm layers covering all skin",
                "Have emergency supplies and blankets in your vehicle"
            ]
            
            is_travel_safe = False
            travel_warning = "Extreme cold presents risks of frostbite, hypothermia, and vehicle breakdown."
            alternative_actions = [
                "Postpone non-essential travel",
                "If travel is necessary, inform others of your route and ETA",
                "Keep emergency heat sources and extra clothing in your vehicle"
            ]
                
        elif temp < 0:
            weather_condition = "cold"
            safety_tips = [
                "Dress in warm layers and cover extremities",
                "Limit time outdoors to prevent hypothermia and frostbite",
                "Keep emergency supplies in your vehicle"
            ]
            
            alternative_actions = [
                "Allow your vehicle to warm up before traveling",
                "Carry extra warm clothing and emergency supplies",
                "Check road conditions before traveling"
            ]
            
        elif wind_speed > 15:
            weather_condition = "windy"
            safety_tips = [
                "Secure loose outdoor objects that could become projectiles",
                "Be cautious of falling branches or debris",
                "Stay away from downed power lines"
            ]
            
            if wind_speed > 20:
                is_travel_safe = False
                travel_warning = "High winds can make vehicle control difficult, especially for high-profile vehicles."
                alternative_actions = [
                    "Postpone travel if driving a high-profile vehicle",
                    "If you must drive, reduce speed and maintain firm grip on steering",
                    "Be extra cautious on bridges and open areas"
                ]
            else:
                alternative_actions = [
                    "Exercise caution when driving, especially high-profile vehicles",
                    "Be alert for debris on roadways",
                    "Check for wind advisories before traveling"
                ]
                
        else:
            # Good weather conditions
            safety_tips = [
                "Stay aware of changing weather conditions",
                "Check forecasts before planning outdoor activities",
                "Have emergency plans updated for your household"
            ]
            
            alternative_actions = [
                "Enjoy outdoor activities while conditions are favorable",
                "Take advantage of good weather for travel",
                "Monitor weather changes throughout the day"
            ]
        
        # 3. Add safety tips section
        response += "🛡️ **Safety Tips**:\n"
        for tip in safety_tips:
            response += f"• {tip}\n"
        response += "\n"
        
        # 4. Add travel recommendation section
        response += "🚗 **Travel Recommendation**:\n"
        if is_travel_safe:
            response += "• Travel appears generally safe at this time.\n"
            response += "• Normal precautions are advised.\n"
            response += "• Stay alert to changing weather conditions.\n"
        else:
            response += f"• ⚠️ Travel not recommended due to {weather_condition} conditions.\n"
            response += f"• {travel_warning}\n"
            response += "• If travel is absolutely necessary, exercise extreme caution.\n"
        response += "\n"
        
        # 5. Add alternative actions section
        response += "💡 **Recommended Actions**:\n"
        for action in alternative_actions:
            response += f"• {action}\n"
            
        return response
    except Exception as e:
        logger.error(f"Error formatting weather response: {str(e)}")
        return "Sorry, I had trouble formatting the weather information. Please try again."

def get_chatbot_response(user_input):
    """
    Generate a response to the user's input based on weather-related keywords,
    providing safety information and travel recommendations.
    
    Args:
        user_input (str): The user's message to the chatbot.
        
    Returns:
        str: The chatbot's response with safety recommendations.
    """
    # Log the user's input
    logger.debug(f"Chatbot received: {user_input}")
    
    # Convert input to lowercase for easier matching
    user_input_lower = user_input.lower()
    
    # Check if this is a weather or travel safety query for a specific city
    city = get_city_from_text(user_input)
    weather_related_terms = ['weather', 'temperature', 'how is', "what's", 'forecast', 'conditions', 'raining', 'snowing']
    travel_related_terms = [
        'travel', 'drive', 'driving', 'road', 'trip', 'commute', 'journey', 'safe to', 'should i go',
        'commuting', 'traffic', 'roads', 'drive to', 'drive in', 'driving to', 'driving in',
        'travel to', 'travel in', 'traveling to', 'traveling in', 'safe for driving',
        'should i drive', 'can i drive', 'ok to drive', 'okay to drive', 'alright to drive'
    ]
    
    if city:
        # Check if it's a weather or travel-related query
        is_weather_query = any(term in user_input_lower for term in weather_related_terms)
        is_travel_query = any(term in user_input_lower for term in travel_related_terms)
        
        if is_weather_query or is_travel_query:
            try:
                logger.debug(f"Detected weather/travel query for city: {city}")
                weather_data = get_weather_data(city, api_key=OPENWEATHER_API_KEY)
                
                # If it's specifically about travel safety, create a more travel-focused response
                response = format_weather_response(weather_data)
                
                if is_travel_query:
                    # Extract key information from the response for a more concise travel summary
                    weather_condition = "normal"
                    description = weather_data['description'].lower()
                    temp = weather_data['temperature']
                    wind_speed = weather_data['wind_speed']
                    is_travel_safe = True
                    
                    # Determine the weather condition category - similar logic as in format_weather_response
                    if 'rain' in description or 'drizzle' in description or 'shower' in description:
                        weather_condition = "rain"
                        if 'heavy' in description or 'thunderstorm' in description:
                            is_travel_safe = False
                    elif 'snow' in description or 'blizzard' in description:
                        weather_condition = "snow"
                        if 'blizzard' in description or 'heavy' in description:
                            is_travel_safe = False
                    elif 'storm' in description or 'thunder' in description:
                        weather_condition = "storm"
                        is_travel_safe = False
                    elif 'fog' in description or 'mist' in description:
                        weather_condition = "fog"
                        if 'dense' in description or 'thick' in description:
                            is_travel_safe = False
                    elif temp > 35:
                        weather_condition = "extreme heat"
                        is_travel_safe = False
                    elif temp < -10:
                        weather_condition = "extreme cold"
                        is_travel_safe = False
                    elif wind_speed > 20:
                        weather_condition = "high winds"
                        is_travel_safe = False
                    
                    # Create a special introduction for travel safety queries
                    travel_intro = f"**🚗 TRAVEL SAFETY ASSESSMENT FOR {weather_data['location'].upper()} 🚗**\n\n"
                    travel_intro += f"You asked about travel safety in {weather_data['location']}. Based on current weather conditions, here is my assessment:\n\n"
                    
                    if is_travel_safe:
                        travel_intro += f"✅ **TRAVEL IS GENERALLY SAFE** under the current {weather_condition} conditions.\n\n"
                    else:
                        travel_intro += f"⚠️ **TRAVEL IS NOT RECOMMENDED** due to {weather_condition} conditions.\n\n"
                    
                    travel_intro += "Below is the detailed weather information and safety recommendations:\n\n"
                    
                    # Add conclusion
                    travel_conclusion = "\n**Additional Travel Advice**:\n"
                    travel_conclusion += "• Check local traffic reports before departing\n"
                    travel_conclusion += "• Ensure your vehicle is properly maintained\n"
                    travel_conclusion += "• Share your travel plans with someone if conditions are concerning\n"
                    travel_conclusion += "• Monitor weather changes throughout your journey\n"
                    
                    return travel_intro + response + travel_conclusion
                else:
                    return response
            except Exception as e:
                logger.error(f"Error getting weather data: {str(e)}")
                return f"I'm sorry, I couldn't retrieve the weather information for {city}. Please check if the city name is correct or try again later."
    
    # Handle travel-related queries without a specific city
    if any(term in user_input_lower for term in travel_related_terms):
        return "To provide travel safety recommendations, I need to know your location. Please ask about travel safety for a specific city, for example: 'Is it safe to travel in Chicago?' or 'What are the travel conditions in New York?'"
    
    # Check for greetings
    if any(greeting in user_input_lower for greeting in ['hello', 'hi', 'hey', 'greetings']):
        return random.choice(GREETINGS)
    
    # Check for farewells
    if any(farewell in user_input_lower for farewell in ['bye', 'goodbye', 'see you', 'thank']):
        return random.choice(FAREWELLS)
    
    # Check for general help or info requests about emergency preparedness
    if any(help_term in user_input_lower for help_term in ['help', 'tips', 'advice', 'prepare', 'emergency', 'safety']):
        return random.choice(GENERAL_TIPS)
    
    # Check for time-related questions
    if re.search(r'\b(time|date|today|now)\b', user_input_lower):
        current_time = datetime.now().strftime("%H:%M")
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        return f"It's currently {current_time} on {current_date}. Remember that weather conditions can change throughout the day, so stay updated with local forecasts."
    
    # Check for specific weather hazards or conditions
    for condition, responses in WEATHER_RESPONSES.items():
        if condition in user_input_lower:
            return random.choice(responses)
    
    # If the query is generally about weather but not specific
    if any(weather_term in user_input_lower for weather_term in ['weather', 'forecast', 'temperature', 'climate', 'rain', 'snow', 'wind']):
        return "I can provide detailed weather safety information and travel recommendations for specific locations. Just ask me questions like:\n• 'What's the weather in Boston?'\n• 'Is it safe to travel in Chicago today?'\n• 'Weather conditions in Miami'\n\nI can also provide specific safety tips for conditions like floods, hurricanes, tornadoes, and more."
    
    # Default response if nothing matches
    return random.choice(UNKNOWN_RESPONSES)
