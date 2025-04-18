import os
import requests
from typing import Optional, Dict, List
from dataclasses import dataclass
from config import Config

@dataclass
class StockInfo:
    symbol: str
    name: str
    price: float
    change: float
    change_percent: float

class StockAPI:
    BASE_URL = "https://www.alphavantage.co/query"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or Config.ALPHAVANTAGE_API_KEY or os.getenv("ALPHAVANTAGE_API_KEY")
        if not self.api_key:
            raise ValueError("Alpha Vantage API key not provided")

    def get_city_stocks(self, city: str) -> Optional[List[StockInfo]]:
        city_to_indices = {
            "London": ["EWU", "ISF.L"],
            "New York": ["SPY", "DIA", "QQQ"],
            "Tokyo": ["NI225"],
            "Hong Kong": ["HSI"],
            "Paris": ["CAC40"],
        }

        symbols = city_to_indices.get(city, ["SPY", "DIA", "QQQ"])
        print(f"Attempting to fetch stock data for: {symbols}")

        stocks = []
        for symbol in symbols:
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': symbol,
                'apikey': self.api_key
            }

            try:
                response = requests.get(self.BASE_URL, params=params)
                response.raise_for_status()
                data = response.json()

                if "Error Message" in data:
                    print(f"API Error for {symbol}: {data['Error Message']}")
                    continue

                quote_data = data.get('Global Quote', {})
                if quote_data and len(quote_data) > 0:
                    stocks.append(StockInfo(
                        symbol=symbol,
                        name=self._get_index_name(symbol),
                        price=float(quote_data.get('05. price', 0)),
                        change=float(quote_data.get('09. change', 0)),
                        change_percent=float(quote_data.get('10. change percent', '0').rstrip('%'))
                    ))
                else:
                    print(f"No quote data available for {symbol}")

            except (requests.exceptions.RequestException, ValueError, KeyError) as e:
                print(f"Error fetching stock data for {symbol}: {e}")
                continue

        return stocks if stocks else None

    def _get_index_name(self, symbol: str) -> str:
        names = {
            "SPY": "S&P 500",
            "DIA": "Dow Jones",
            "QQQ": "NASDAQ"
        }
        return names.get(symbol, symbol)
