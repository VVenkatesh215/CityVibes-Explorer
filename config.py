import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "your-default-key")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY", "your-default-key")
    FOURSQUARE_API_KEY = os.getenv("FOURSQUARE_API_KEY", "your-default-key")
    ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", "your-default-key")
    EVENTBRITE_API_KEY = os.getenv("EVENTBRITE_API_KEY", "your-default-key")
    
    REQUEST_TIMEOUT = 10 
    CACHE_EXPIRY = 3600