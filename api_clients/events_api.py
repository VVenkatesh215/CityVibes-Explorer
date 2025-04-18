import os
import requests
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from config import Config

@dataclass
class Event:
    name: str
    venue: str
    date: datetime
    price: Optional[str]
    url: str

class EventbriteAPI:
    BASE_URL = "https://www.eventbriteapi.com/v3/events/search"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or Config.EVENTBRITE_API_KEY
        if not self.api_key:
            raise ValueError("Eventbrite API key not provided")
    
    def get_city_events(self, city: str, limit: int = 5) -> Optional[List[Event]]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json"
        }
        params = {
            "location.address": city,
            "expand": "venue",
            "sort_by": "date",
            "limit": limit
        }
        
        try:
            status_response = requests.get(
                "https://www.eventbriteapi.com/v3/system/status/",
                headers=headers
            )
            if status_response.status_code != 200:
                print(f"Eventbrite API may be unavailable: {status_response.status_code}")
                return self._get_fallback_events(city)
            
            response = requests.get(
                self.BASE_URL,
                headers=headers,
                params=params
            )

            if response.status_code == 404:
                print("Trying alternative endpoint (not implemented here)")
                return self._get_fallback_events(city)

            response.raise_for_status()
            data = response.json()

            events = []
            for event in data.get('events', []):
                try:
                    events.append(Event(
                        name=event['name']['text'],
                        venue=event.get('venue', {}).get('name', 'Online Event'),
                        date=datetime.strptime(event['start']['local'], '%Y-%m-%dT%H:%M:%S'),
                        price="Free" if event.get('is_free', False) else "Paid",
                        url=event['url']
                    ))
                except KeyError as e:
                    print(f"Skipping event due to missing data: {e}")
                    continue
            
            if not events:
                print("Using fallback event data")
                return self._get_fallback_events(city)

            return events

        except requests.exceptions.RequestException as e:
            error_msg = e.response.json() if hasattr(e, 'response') else str(e)
            print(f"Eventbrite API Error: {error_msg}")
            return self._get_fallback_events(city)
    
    def _get_fallback_events(self, city: str) -> Optional[List[Event]]:
        fallback_events = {
            "New York": [
                Event(
                    name="Broadway Show - Hamilton",
                    venue="Richard Rodgers Theatre",
                    date=datetime.now() + timedelta(days=2),
                    price="$199+",
                    url="https://example.com/events/hamilton"
                ),
                Event(
                    name="Central Park Summer Concert Series",
                    venue="Central Park Great Lawn",
                    date=datetime.now() + timedelta(days=5),
                    price="Free",
                    url="https://example.com/events/cpconcert"
                ),
            ],
            "London": [
                Event(
                    name="West End Musical - Les Misérables",
                    venue="Queen's Theatre",
                    date=datetime.now() + timedelta(days=1),
                    price="£45+",
                    url="https://example.com/events/lesmis"
                ),
                Event(
                    name="Hyde Park Summer Festival",
                    venue="Hyde Park",
                    date=datetime.now() + timedelta(days=7),
                    price="£25",
                    url="https://example.com/events/hydepark"
                ),
            ],
        }
        return fallback_events.get(city)
