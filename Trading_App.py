import streamlit as st
import yfinance as yf
from PIL import Image
from datetime import datetime

# Fetch live market data using yfinance
def get_market_data():
    tickers = {
        "S&P 500": "^GSPC",
        "NASDAQ": "^IXIC",
        "DOW JONES": "^DJI",
       
    }

    try:
        data = yf.download(list(tickers.values()), period="1d", interval="1m", group_by="ticker")
        if data.empty:
            # fallback if data unavailable
            data = yf.download(list(tickers.values()), period="5d", interval="1d", group_by="ticker")
    except:
        return {k: {'last': 'N/A', 'change': 'N/A', 'status': 'neutral'} for k in tickers.keys()}

    latest_data = {}
    for name, symbol in tickers.items():
        try:
            df = data[symbol]
            last = df['Close'].dropna().iloc[-1]
            prev = df['Close'].dropna().iloc[-5]
            change = ((last - prev) / prev) * 100
            latest_data[name] = {
                'last': round(last, 2),
                'change': round(change, 2),
                'status': 'up' if change > 0 else 'down'
            }
        except:
            latest_data[name] = {'last': 'N/A', 'change': 'N/A', 'status': 'neutral'}
    return latest_data


# Streamlit configuration
st.set_page_config(page_title="EquiNova", page_icon="🌠", layout="wide")

# Styling
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

# Heading
st.markdown("""
    <div style="text-align:center; margin-top: -10px; margin-bottom: 30px;">
        <h1 style="font-size: 52px; font-weight: 900; color: #1a3669; font-family: 'Poppins', sans-serif;">
            🌠 EquiNova
        </h1>
        <p style="font-size: 18px; color: #444; margin-top: -10px; font-family: 'Poppins', sans-serif;">
            Illuminate your trades with data-driven foresight
        </p>
    </div>
""", unsafe_allow_html=True)


# Banner Image
try:
    image = Image.open("app.png")
    st.image(image, use_container_width=True)
except:
    st.warning("📷 Please ensure 'app.png' exists in your app directory")

# Live Market Overview (moved below image)
st.markdown("## 🚦 TradeSignals")
market_data = get_market_data()
col1, col2, col3, col4 = st.columns(4)
cols = [col1, col2, col3, col4]

for idx, (name, details) in enumerate(market_data.items()):
    with cols[idx]:
        st.markdown(f"<div class='stat-card'>"
                    f"<div>{name}</div>"
                    f"<div class='stat-value'>{details['last']}</div>"
                    f"<div class='{'stat-change-up' if details['status']=='up' else 'stat-change-down'}'>"
                    f"{'🔺' if details['status']=='up' else '🔻'} {details['change']}%"
                    f"</div></div>", unsafe_allow_html=True)

# Our Services
st.markdown("## 🌟Key Offerings")
col1, col2 , col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class='feature-card'>
        <h3>📊 Market Pulse</h3>
        <p>Dive into real-time market movements, financial insights, and technical indicators. Track historical trends, analyze stock fundamentals, and make informed trading decisions — all powered by live data from Yahoo Finance.</p>
    </div>
""", unsafe_allow_html=True)


with col2:
    st.markdown("""
        <div class='feature-card'>
            <h3>🔮 Price Forecast</h3>
            <p>Uncover future price movements with precision-driven forecasts based on historical patterns and statistical trends. Empower your trading decisions with data-backed projections designed to give you a confident edge in the market.</p>
        </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class='feature-card'>
        <h3>🚨 Trade Alert</h3>
        <p>Spot market shocks before they settle. Powered by anomaly detection, Trade Alert pinpoints unusual price surges and drops — giving you real-time signals wrapped in intuitive visuals and smart insights.</p>
    </div>
    """, unsafe_allow_html=True)


# How It Works
st.markdown("## 🧭 Your Trading Journey")
col1, col2, col3,col4 = st.columns(4)

with col1:
    st.markdown("""
        <div class='feature-card'>
            <h4>1️⃣ Discover Your Stock</h4>
            <p>Effortlessly explore top-performing stocks or enter your own ticker to begin a personalized analysis journey.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class='feature-card'>
            <h4>2️⃣ Decode Market Movements</h4>
            <p>Dive into historical trends, compare technical indicators, and extract financial metrics that matter most.</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class='feature-card'>
            <h4>3️⃣ Unlock Future Predictions</h4>
            <p>Visualize intelligent 30-day projections that help guide your timing, strategy, and confidence in trades.</p>
        </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown("""
        <div class='feature-card'>
            <h4>4️⃣ Spot Market Anomalies</h4>
            <p>Catch unusual price spikes or dips in real time with smart Z-score-based detection to enhance trade decisions.</p>
        </div>
    """, unsafe_allow_html=True)