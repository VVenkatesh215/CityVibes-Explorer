# CityVibes Explorer

**CityVibes Explorer** is a Python-based CLI tool that brings together data from public APIs to give you a snapshot of a city's daily vibe. From weather and news to stock indices, tourist spots, and local events this tool provides a blend of insights, all in one terminal screen.

---

## Project Overview

This project was built to demonstrate creativity and the ability to blend multiple public data sources into a cohesive, interpretable format.

When you input a city name, the tool fetches and combines information such as:
- Weather conditions  
- Top news headlines  
- Local stock indices  
- Popular attractions  
- Upcoming local events  

---

## Public APIs Used

1. **OpenWeatherMap API** – for real time weather data  
   https://openweathermap.org/api  
2. **NewsAPI** – for latest headlines  
   https://newsapi.org/  
3. **Eventbrite API** – for upcoming local events  
   https://www.eventbrite.com/platform/api  
4. **Foursquare Places API** – for popular tourist spots  
   https://developer.foursquare.com/docs  
5. **ALPHAVANTAGE API** – for stock indices (S&P 500, Dow Jones, Nasdaq)  
   https://pypi.org/project/yfinance/  

---

## Project Structure
city_vibes_explorer/
│
├── data/
│ ├── delhi_vibes.json
│ ├── london_vibes.json
│ └── ...
│
├── tests/
│ └── test_apis.py # Basic tests for core functions
│
├── events_api.py # Eventbrite API logic
├── foursquare_api.py # Foursquare logic
├── news_api.py # NewsAPI integration
├── stock_api.py # Stock data using yfinance
├── weather_api.py # Weather API integration
├── config.py # API key management
├── main.py # Entry point / CLI
├── requirements.txt
├── .env # Environment file for storing API keys
└── README.md

---

## Installation & Setup

1. Clone the Repository
```bash
git clone https://github.com/your-username/city-vibes.git
cd city-vibes


Install Requirements
```bash
pip install -r requirements.txt


Set Environment Variables
Create a .env file in the root directory with the following format:
```bash
WEATHER_API_KEY=your_openweathermap_key
NEWS_API_KEY=your_newsapi_key
EVENTBRITE_API_KEY=your_eventbrite_key
FOURSQUARE_API_KEY=your_foursquare_key
FMP_API_KEY=your_financialmodelingprep_key
Note: The .env file is ignored via .gitignore.

---
Bonus Features:
Modular, testable code
Rate limit handling and retries
Environment variable security
Caching for performance boost