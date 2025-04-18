import os
import requests
from typing import Optional, List, Dict
from dataclasses import dataclass
from datetime import datetime

@dataclass
class NewsArticle:
    title: str
    description: str
    source: str
    published_at: datetime
    url: str

class NewsAPI:
    BASE_URL = "https://newsapi.org/v2/everything"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("NEWS_API_KEY")
        if not self.api_key:
            raise ValueError("News API key not provided")
    
    # api_clients/news_api.py
    def get_city_news(self, city: str, limit: int = 5) -> Optional[List[NewsArticle]]:
        params = {
        'q': city,
        'apiKey': self.api_key,
        'pageSize': limit,
        'sortBy': 'publishedAt',
        'language': 'en', 
        'domains': 'bbc.co.uk,cnn.com,nytimes.com' 
    }
        
        try:
            response = requests.get(self.BASE_URL, params=params)
            #print("News API Response:", response.json())  
            response.raise_for_status()
            data = response.json()
                
            articles = []
            for article in data.get('articles', []):
                articles.append(NewsArticle(
                        title=article['title'],
                        description=article['description'],
                        source=article['source']['name'],
                        published_at=datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'),
                        url=article['url']
                    ))
                
                return articles
        except (requests.exceptions.RequestException, KeyError) as e:
                print(f"Error fetching news for {city}: {e}")
                return None