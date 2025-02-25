import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.stock_data import get_stock_data
from utils.technical_analysis import calculate_indicators
from utils.recommendations import generate_recommendation
from utils.news_data import get_financial_news

# List of common stock symbols and their names
STOCK_SUGGESTIONS = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corporation",
    "GOOGL": "Alphabet Inc.",
    "AMZN": "Amazon.com Inc.",
    "META": "Meta Platforms Inc.",
    "TSLA": "Tesla Inc.",
    "NVDA": "NVIDIA Corporation",
    "JPM": "JPMorgan Chase & Co.",
    "BAC": "Bank of America Corp.",
    "WMT": "Walmart Inc.",
    "JNJ": "Johnson & Johnson",
    "PG": "Procter & Gamble Co.",
    "HD": "Home Depot Inc.",
    "DIS": "Walt Disney Co.",
    "NFLX": "Netflix Inc."
}

# Page config
st.set_page_config(
    page_title="Stock Analysis & Recommendations",
    layout="wide"
)

# Title and description
st.title("📈 Stock Analysis & Recommendations")
st.markdown("""
This app provides technical analysis and recommendations for stocks based on various indicators.
Select a stock symbol from the suggestions or enter a custom one!
""")

# Stock symbol input with suggestions
symbol = st.selectbox(
    "Enter Stock Symbol",
    options=list(STOCK_SUGGESTIONS.keys()),
    format_func=lambda x: f"{x} - {STOCK_SUGGESTIONS[x]}",
    index=0
).upper()

try:
    # Date range selection
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            datetime.now() - timedelta(days=365)
        )
    with col2:
        end_date = st.date_input("End Date", datetime.now())

    if st.button("Analyze Stock"):
        with st.spinner("Fetching stock data..."):
            # Get stock data
            df = get_stock_data(symbol, start_date, end_date)

            # Calculate technical indicators
            df = calculate_indicators(df)

            # Generate recommendation
            recommendation, confidence, reasons = generate_recommendation(df)

            # Display recommendation
            rec_color = "green" if recommendation == "BUY" else "red" if recommendation == "SELL" else "orange"
            st.header("Recommendation")
            st.markdown(f"""
            <div style='background-color: {rec_color}30; padding: 20px; border-radius: 10px;'>
                <h2 style='color: {rec_color}; margin:0;'>{recommendation}</h2>
                <p>Confidence: {confidence}%</p>
            </div>
            """, unsafe_allow_html=True)

            # Display reasons
            st.subheader("Analysis Breakdown")
            for reason in reasons:
                st.markdown(f"• {reason}")

            # Create price chart
            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name='Price'
            ))

            # Add moving averages
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['SMA_20'],
                name='20-day SMA',
                line=dict(color='orange')
            ))

            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['SMA_50'],
                name='50-day SMA',
                line=dict(color='blue')
            ))

            fig.update_layout(
                title=f'{symbol} - {STOCK_SUGGESTIONS.get(symbol, "Stock")} Price',
                yaxis_title='Price',
                xaxis_title='Date',
                template='plotly_white'
            )

            st.plotly_chart(fig, use_container_width=True)

            # Technical indicators charts
            col1, col2 = st.columns(2)

            with col1:
                # RSI Chart
                fig_rsi = go.Figure()
                fig_rsi.add_trace(go.Scatter(
                    x=df.index,
                    y=df['RSI'],
                    name='RSI'
                ))
                fig_rsi.add_hline(y=70, line_color="red")
                fig_rsi.add_hline(y=30, line_color="green")
                fig_rsi.update_layout(
                    title='RSI Indicator',
                    yaxis_title='RSI',
                    template='plotly_white'
                )
                st.plotly_chart(fig_rsi, use_container_width=True)

            with col2:
                # MACD Chart
                fig_macd = go.Figure()
                fig_macd.add_trace(go.Scatter(
                    x=df.index,
                    y=df['MACD'],
                    name='MACD'
                ))
                fig_macd.add_trace(go.Scatter(
                    x=df.index,
                    y=df['Signal_Line'],
                    name='Signal Line'
                ))
                fig_macd.update_layout(
                    title='MACD Indicator',
                    yaxis_title='MACD',
                    template='plotly_white'
                )
                st.plotly_chart(fig_macd, use_container_width=True)

            # Key metrics
            st.subheader("Key Metrics")
            metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)

            with metrics_col1:
                st.metric("Current Price", f"${df['Close'].iloc[-1]:.2f}")
            with metrics_col2:
                price_change = ((df['Close'].iloc[-1] - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100
                st.metric("Daily Change", f"{price_change:.2f}%")
            with metrics_col3:
                st.metric("Volume", f"{df['Volume'].iloc[-1]:,.0f}")
            with metrics_col4:
                st.metric("RSI", f"{df['RSI'].iloc[-1]:.2f}")

            # Add News Section
            st.subheader("📰 Latest Financial News")
            with st.spinner("Fetching latest news..."):
                # Get news for the selected stock and general market news
                news_items = get_financial_news([symbol])

                if news_items:
                    for news in news_items:
                        with st.expander(f"📑 {news['title']}", expanded=False):
                            st.write(f"**Source:** {news.get('publisher', 'Yahoo Finance')}")
                            st.write(f"**Published:** {datetime.fromtimestamp(news['providerPublishTime']).strftime('%Y-%m-%d %H:%M:%S')}")
                            st.write(news.get('description', 'No description available'))
                            if 'link' in news:
                                st.markdown(f"[Read more]({news['link']})")
                else:
                    st.info("No recent news available.")

except Exception as e:
    st.error(f"Error: {str(e)}")
    st.info("Please check the stock symbol and try again.")