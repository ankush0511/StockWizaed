import yfinance as yf
from typing import List, Dict
import pandas as pd

def get_financial_news(symbols: List[str] = None) -> List[Dict]:
    """
    Fetch financial news from Yahoo Finance
    If symbols is provided, fetch news for those specific stocks
    Otherwise fetch general market news
    """
    try:
        news_items = []
        
        # If no symbols provided, use market indices to get general news
        if not symbols:
            symbols = ['^GSPC', '^DJI', '^IXIC']  # S&P 500, Dow Jones, NASDAQ
            
        for symbol in symbols:
            ticker = yf.Ticker(symbol)
            news = ticker.news
            if news:
                news_items.extend(news)
        
        # Sort by publish date and remove duplicates
        if news_items:
            df = pd.DataFrame(news_items)
            df = df.drop_duplicates(subset=['title'])
            df = df.sort_values('providerPublishTime', ascending=False)
            return df.head(10).to_dict('records')
        
        return []
        
    except Exception as e:
        print(f"Error fetching news: {str(e)}")
        return []
