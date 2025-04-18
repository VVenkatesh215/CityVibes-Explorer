import os
import requests
from typing import Optional, List
from dataclasses import dataclass

@dataclass
class Venue:
    name: str
    address: str
    category: str
    rating: Optional[float]
    price_level: Optional[int] 

class FoursquareAPI:
    BASE_URL = "https://api.foursquare.com/v3/places/search"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("FOURSQUARE_API_KEY")
        if not self.api_key:
            raise ValueError("Foursquare API key not provided")
    
    def get_places(self, city: str, category: str = "tourist_attraction", limit: int = 5) -> Optional[List[Venue]]:
        headers = {
            "Accept": "application/json",
            "Authorization": self.api_key
        }
        
        params = {
                    "near": city,
                    "categories": "16000",  
                    "limit": limit,
                    "fields": "name,location,rating,price,categories"
                }
        
        try:
            response = requests.get(self.BASE_URL, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            venues = []
            for venue in data.get('results', []):
                venues.append(Venue(
                    name=venue['name'],
                    address=venue['location'].get('formatted_address', ''),
                    category=venue['categories'][0]['name'] if venue.get('categories') else 'Unknown',
                    rating=venue.get('rating'),
                    price_level=venue.get('price', {}).get('tier')
                ))
            
            return venues
        except (requests.exceptions.RequestException, KeyError) as e:
            print(f"Error fetching Foursquare places for {city}: {e}")
            return None