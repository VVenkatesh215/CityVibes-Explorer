import os
import requests
from typing import Optional
from dataclasses import dataclass

@dataclass
class WeatherData:
    temperature: float
    conditions: str
    humidity: int
    wind_speed: float
    city: str

class WeatherAPI:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            raise ValueError("OpenWeather API key not provided")
    
    def get_weather(self, city: str) -> Optional[WeatherData]:
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            return WeatherData(
                temperature=data['main']['temp'],
                conditions=data['weather'][0]['description'],
                humidity=data['main']['humidity'],
                wind_speed=data['wind']['speed'],
                city=city
            )
        except (requests.exceptions.RequestException, KeyError) as e:
            print(f"Error fetching weather for {city}: {e}")
            return None