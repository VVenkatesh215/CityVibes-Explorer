from config import Config
from api_clients.weather_api import WeatherAPI
from api_clients.news_api import NewsAPI
from api_clients.foursquare_api import FoursquareAPI
from api_clients.stock_api import StockAPI
from api_clients.events_api import EventbriteAPI
import argparse
from datetime import datetime
import json
import os

def display_city_vibes(city: str):
    print(f"\n\U0001F306 Gathering City Vibes for {city}...\n")

    try:
        weather = WeatherAPI(Config.OPENWEATHER_API_KEY).get_weather(city)
        news = NewsAPI(Config.NEWS_API_KEY).get_city_news(city)
        places = FoursquareAPI(Config.FOURSQUARE_API_KEY).get_places(city)
        stocks = StockAPI(Config.ALPHAVANTAGE_API_KEY).get_city_stocks(city)
        events = EventbriteAPI(Config.EVENTBRITE_API_KEY).get_city_events(city)

        display_weather(weather)
        display_news(news)
        display_places(places)
        display_stocks(stocks)
        display_events(events)

        save_city_vibes_to_json(city, {
            "weather": weather.__dict__ if weather else None,
            "news": [article.__dict__ for article in news] if news else [],
            "places": [place.__dict__ for place in places] if places else [],
            "stocks": [stock.__dict__ for stock in stocks] if stocks else [],
            "events": [event.__dict__ for event in events] if events else []
        })

    except Exception as e:
        print(f"\n\u26A0\ufe0f Error: {str(e)}")
        print("Some data may be incomplete. Check your API keys.")

def display_weather(weather):
    print("\U0001F326 Weather:")
    if weather:
        print(f"{weather.temperature}°C, {weather.conditions}")
        print(f"💧 Humidity: {weather.humidity}% | 💨 Wind: {weather.wind_speed} m/s")
    else:
        print("No weather data")

def display_news(news):
    print("\n📰 Top News Headlines:")
    if news:
        for i, article in enumerate(news[:3], 1):
            pub_date = article.published_at.strftime('%b %d, %Y')
            print(f"{i}. {article.title} ({article.source})")
            print(f"   📅 {pub_date}")
            print(f"   📓 {article.description[:100]}...\n")
    else:
        print("No news available")

def display_places(places):
    print("\n🏟 Popular Places:")
    if places:
        for i, place in enumerate(places[:3], 1):
            price_display = '💲' * (place.price_level if place.price_level is not None else 1)
            print(f"{i}. {place.name}")
            print(f"   🏷 Category: {place.category}")
            print(f"   ⭐ Rating: {place.rating if place.rating is not None else 'N/A'}")
            print(f"   💲 Price: {price_display} (Level: {place.price_level if place.price_level is not None else 'N/A'})")
    else:
        print("No places data available")

def display_stocks(stocks):
    print("\n📈 Local Stock Indices:")
    if stocks:
        for stock in stocks:
            trend = "↑" if stock.change_percent >= 0 else "↓"
            print(f"{stock.name}: {stock.price} ({trend}{abs(stock.change_percent)}%)")
    else:
        print("No stock data available")

def display_events(events):
    print("\n🎟 Upcoming Events:")
    if events:
        for i, event in enumerate(events[:3], 1):
            print(f"{i}. {event.name}")
            print(f"   📍 {event.venue}")
            print(f"   🗓 {event.date.strftime('%a %b %d')}")
            print(f"   💵 {event.price or 'Price varies'}\n")
    else:
        print("No upcoming events found")

def save_city_vibes_to_json(city, data):
    os.makedirs("data", exist_ok=True)
    filename = f"data/{city.lower().replace(' ', '_')}_vibes.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, default=str)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="City Vibes Explorer")
    parser.add_argument("--city", required=True, help="City name to explore")
    args = parser.parse_args()

    display_city_vibes(args.city)
