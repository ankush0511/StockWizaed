import yfinance as yf
import pandas as pd

def get_stock_data(symbol: str, start_date, end_date) -> pd.DataFrame:
    """
    Fetch stock data from Yahoo Finance
    """
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(start=start_date, end=end_date)
        
        if df.empty:
            raise ValueError("No data found for this symbol")
            
        return df
        
    except Exception as e:
        raise Exception(f"Error fetching data for {symbol}: {str(e)}")
