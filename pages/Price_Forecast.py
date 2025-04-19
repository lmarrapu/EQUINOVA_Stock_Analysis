import streamlit as st
import pandas as pd
from pages.utils.model_train import (
    get_data, get_rolling_mean, get_differencing_order,
    scaling, evaluate_model, get_forecast, inverse_scaling
)
from pages.utils.plotly_figure import plotly_table, Moving_average_forecast

# Streamlit config
st.set_page_config(
    page_title="Price Forecast",
    page_icon="🔮",
    layout="wide"
)

st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
            background-color: #f4f7fa;
        }
        .title-style {
            font-size: 48px;
            font-weight: 800;
            text-align: center;
            color: #1a3669;
            margin-top: 10px;
        }
        .subtitle-style {
            font-size: 20px;
            text-align: center;
            color: #444;
            margin-bottom: 30px;
        }
        .stat-card {
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            padding: 20px;
            text-align: center;
            transition: 0.3s ease;
        }
        .stat-card:hover {
            box-shadow: 0 0 15px #9acaa6;
            transform: translateY(-4px);
        }
        .stat-value {
            font-size: 30px;
            font-weight: 700;
            color: #1a3669;
        }
        .stat-change-up {
            color: green;
            font-weight: 600;
        }
        .stat-change-down {
            color: red;
            font-weight: 600;
        }
        .feature-card {
            background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
            border: 1px solid #e9ecef;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            height: 100%;
            transition: 0.3s ease;
        }
        .feature-card:hover {
            box-shadow: 0 0 15px #9acaa6;
            transform: translateY(-6px);
        }
        .stSidebar {
            background-color: #b2d8c2 !important;
            background-image: linear-gradient(to bottom, #b2d8c2, #9acaa6);
        }
    </style>
""", unsafe_allow_html=True)


st.title("🔮 Price Forecast")

# Stock Ticker Selection (Dropdown + Manual Entry)
famous_tickers = ['TSLA', 'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'META', 'NFLX', 'NVDA', 'IBM']
col1, col2 = st.columns([2, 2])

with col1:
    ticker_dropdown = st.selectbox("Choose from Popular Tickers", famous_tickers)
with col2:
    custom_ticker = st.text_input("Or enter a custom ticker", "")

# Final ticker to use
ticker = custom_ticker.strip().upper() if custom_ticker else ticker_dropdown

# Load and process data
close_price = get_data(ticker)
rolling_price = get_rolling_mean(close_price)

st.markdown(f"### 📅 30-Day Smart Forecast for {ticker}")

try:
    differencing_order = get_differencing_order(rolling_price)
    scaled_data, scaler = scaling(rolling_price)

    rmse = evaluate_model(scaled_data, differencing_order)

    forecast = get_forecast(scaled_data, differencing_order)
    forecast['Close'] = inverse_scaling(scaler, forecast['Close'])

    # 📊 Relative RMSE
    mean_price = float(close_price['Close'].iloc[-30:].mean())
    rel_rmse = (rmse / mean_price) * 100

    st.success(f"📊 RMSE Score: **{rmse}**")
    st.info(f"📉 Relative RMSE: **{rel_rmse:.2f}%** of avg. price (${mean_price:.2f})")

    st.markdown("#### 🌐 Predictive Outlook")
    forecast_rounded = forecast.round(2)
    st.plotly_chart(plotly_table(forecast_rounded), use_container_width=True)

    # ✅ Combine historical and forecast data for full visualization
    historical_df = rolling_price.copy()
    historical_df.columns = ['Close']
    combined_df = pd.concat([historical_df, forecast])

    display_start = max(0, len(combined_df) - 180)
    st.markdown("#### 🔍 Future Insights")
    st.plotly_chart(Moving_average_forecast(combined_df.iloc[display_start:]), use_container_width=True)

except Exception as e:
    st.error(f"❌ Forecasting failed: {e}")