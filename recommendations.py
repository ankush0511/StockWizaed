import pandas as pd

def generate_recommendation(df: pd.DataFrame) -> tuple:
    """
    Generate buy/sell recommendation based on technical indicators
    Returns: (recommendation, confidence, reasons)
    """
    reasons = []
    buy_signals = 0
    sell_signals = 0
    total_signals = 0
    
    # Check RSI
    current_rsi = df['RSI'].iloc[-1]
    if current_rsi < 30:
        buy_signals += 1
        reasons.append(f"RSI is oversold ({current_rsi:.2f})")
    elif current_rsi > 70:
        sell_signals += 1
        reasons.append(f"RSI is overbought ({current_rsi:.2f})")
    total_signals += 1
    
    # Check MACD
    if df['MACD'].iloc[-1] > df['Signal_Line'].iloc[-1] and \
       df['MACD'].iloc[-2] <= df['Signal_Line'].iloc[-2]:
        buy_signals += 1
        reasons.append("MACD crossed above signal line")
    elif df['MACD'].iloc[-1] < df['Signal_Line'].iloc[-1] and \
         df['MACD'].iloc[-2] >= df['Signal_Line'].iloc[-2]:
        sell_signals += 1
        reasons.append("MACD crossed below signal line")
    total_signals += 1
    
    # Check Moving Averages
    if df['SMA_20'].iloc[-1] > df['SMA_50'].iloc[-1] and \
       df['SMA_20'].iloc[-2] <= df['SMA_50'].iloc[-2]:
        buy_signals += 1
        reasons.append("Short-term MA crossed above long-term MA")
    elif df['SMA_20'].iloc[-1] < df['SMA_50'].iloc[-1] and \
         df['SMA_20'].iloc[-2] >= df['SMA_50'].iloc[-2]:
        sell_signals += 1
        reasons.append("Short-term MA crossed below long-term MA")
    total_signals += 1
    
    # Check price relative to Bollinger Bands
    if df['Close'].iloc[-1] < df['BB_lower'].iloc[-1]:
        buy_signals += 1
        reasons.append("Price below lower Bollinger Band")
    elif df['Close'].iloc[-1] > df['BB_upper'].iloc[-1]:
        sell_signals += 1
        reasons.append("Price above upper Bollinger Band")
    total_signals += 1
    
    # Calculate confidence and recommendation
    if buy_signals > sell_signals:
        confidence = (buy_signals / total_signals) * 100
        recommendation = "BUY"
    elif sell_signals > buy_signals:
        confidence = (sell_signals / total_signals) * 100
        recommendation = "SELL"
    else:
        confidence = 50
        recommendation = "HOLD"
        reasons.append("Technical indicators are neutral")
    
    return recommendation, confidence, reasons
