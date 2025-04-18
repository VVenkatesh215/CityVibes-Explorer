import unittest
from config import Config
from api_clients.weather_api import WeatherAPI, WeatherData 

class TestAPIs(unittest.TestCase):
    def test_weather(self):
        weather = WeatherAPI(Config.OPENWEATHER_API_KEY).get_weather("London")
        self.assertIsNotNone(weather, "Weather API returned None - check your API key")
        
        if weather is not None:
            self.assertIsInstance(weather, WeatherData, 
                                f"Expected WeatherData, got {type(weather)}")
            
            self.assertIsInstance(weather.temperature, float)
            self.assertIsInstance(weather.conditions, str)

if __name__ == "__main__":
    unittest.main()