import streamlit as st
import yfinance as yf
import datetime
import pandas as pd
from pages.utils.plotly_figure import plotly_table, candlestick, RSI, close_chart, Moving_average, MACD

# Page config
st.set_page_config(
    page_title="Market Pulse",
    page_icon="📊",
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
            margin-top: -10px;
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


st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
            background-color: #f4f7fa;
        }
        .section-title {
            font-size: 26px;
            font-weight: 600;
            color: #1f77b4;
            margin-top: 30px;
            margin-bottom: 10px;
        }
        .metric-box {
            background-color: #ffffff;
            padding: 10px 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }
    </style>
""", unsafe_allow_html=True)
st.markdown("""
    <style>
        .stButton > button {
            background-color: #9acaa6;  /* Soft green matching sidebar */
            color: black;
            font-weight: bold;
            border-radius: 8px;
            padding: 8px 20px;
            transition: all 0.3s ease-in-out;
            border: none;
        }
        .stButton > button:hover {
            background-color: #FFD700;  /* Shiny gold */
            color: black;
            transform: translateY(-2px);
            box-shadow: 0 0 10px #FFD700;
        }
    </style>
""", unsafe_allow_html=True)


st.title("📊Market Pulse")

# -------------------- Ticker Selection --------------------
# --- Popular Ticker Dictionary ---
popular_tickers = {
    "Apple (AAPL)": "AAPL",
    "Tesla (TSLA)": "TSLA",
    "Microsoft (MSFT)": "MSFT",
    "Amazon (AMZN)": "AMZN",
    "Google (GOOGL)": "GOOGL",
    "Meta (META)": "META",
    "NVIDIA (NVDA)": "NVDA",
    "Netflix (NFLX)": "NFLX",
    "Berkshire Hathaway (BRK-B)": "BRK-B"
}

st.markdown("### 📌 Choose a Stock to Analyze")

col1, col2, col3 = st.columns(3)
today = datetime.date.today()

# --- Stock Selection ---
with col1:
    ticker_dropdown = st.selectbox("📂 Select from Popular Stocks", list(popular_tickers.keys()))
    custom_ticker = st.text_input("✍️ Or enter a custom ticker", "")
    ticker = custom_ticker.strip().upper() if custom_ticker else popular_tickers[ticker_dropdown]

# --- Date Range Selection ---
with col2:
    start_date = st.date_input("📅 Start Date", datetime.date(today.year - 1, today.month, today.day))
with col3:
    end_date = st.date_input("📅 End Date", today)

# --- Company Information Display ---
st.markdown(f"<h3 class='section-title'>🏢 Company Overview: <span style='color:#1a3669'>{ticker}</span></h3>", unsafe_allow_html=True)

try:
    stock = yf.Ticker(ticker)
    info = stock.info

    st.markdown(f"""
        <div style="background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 25px;">
            <p style="font-size: 16px; line-height: 1.6; color: #333;">{info.get('longBusinessSummary', 'No summary available.')}</p>
            <hr style="border: none; border-top: 1px solid #eee; margin: 15px 0;">
            <p><strong>🏷️ Sector:</strong> {info.get('sector', 'N/A')}</p>
            <p><strong>👥 Full-Time Employees:</strong> {info.get('fullTimeEmployees', 'N/A')}</p>
            <p><strong>🌐 Website:</strong> <a href="{info.get('website', '#')}" target="_blank">{info.get('website', 'N/A')}</a></p>
        </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.warning("⚠️ Unable to retrieve company information. Please try a different ticker.")

# -------------------- Financial Metrics --------------------
st.markdown("<h3 class='section-title'>📈 Financial Metrics</h3>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    try:
        metrics = [
            ('Market Cap', 'marketCap', lambda x: f"${x:,}" if x else 'N/A'),
            ('Beta', 'beta', lambda x: round(x, 2) if x else 'N/A'),
            ('EPS', 'trailingEps', lambda x: round(x, 2) if x else 'N/A'),
            ('PE Ratio', 'trailingPE', lambda x: round(x, 2) if x else 'N/A')
        ]
        values = [formatter(stock.info.get(key)) for _, key, formatter in metrics]
        df = pd.DataFrame({'Value': values}, index=[label for label, _, _ in metrics])
        df.index.name = 'Metric'
        st.plotly_chart(plotly_table(df), use_container_width=True)
    except Exception as e:
        st.error(f"Error fetching key metrics: {e}")

with col2:
    try:
        df = pd.DataFrame(index=['Quick Ratio', 'Revenue/Share', 'Profit Margins', 'Debt to Equity', 'ROE'])
        df['Value'] = [
            stock.info.get("quickRatio", 'N/A'),
            stock.info.get("revenuePerShare", 'N/A'),
            stock.info.get("profitMargins", 'N/A'),
            stock.info.get("debtToEquity", 'N/A'),
            stock.info.get("returnOnEquity", 'N/A')
        ]
        df.index.name = 'Metric'
        st.plotly_chart(plotly_table(df), use_container_width=True)
    except:
        st.warning("Some financial ratios may not be available for this stock.")

# -------------------- Historical Table --------------------
st.markdown("### Last 10 Days Performance")


data = yf.download(ticker, start=start_date, end=end_date)

try:
    last_10_df = data.tail(10).sort_index(ascending=False).round(2)
    last_10_df = last_10_df.reset_index()
    last_10_df['Date'] = last_10_df['Date'].dt.strftime('%b %d, %Y')
    last_10_df.columns = [col if isinstance(col, str) else ' '.join(col).strip() for col in last_10_df.columns]
    st.plotly_chart(plotly_table(last_10_df), use_container_width=True)
except Exception as e:
    st.warning(f"❗ Unable to display historical table: {e}")

# -------------------- Chart Period Selection --------------------
st.markdown("### Chart Explorer")
col_btn = st.columns(6)
period_options = ['5d', '1mo', '6mo', '1y', '5y', 'max']
selected_period = st.session_state.get('period', '1y')

for i, label in enumerate(['5D', '1M', '6M', '1Y', '5Y', 'MAX']):
    if col_btn[i].button(label):
        selected_period = period_options[i]
        st.session_state['period'] = selected_period

# -------------------- Chart Controls --------------------
col_chart1, col_chart2 = st.columns(2)
with col_chart1:
    chart_type = st.selectbox("📈 Chart Type", ['Candle', 'Line'])
with col_chart2:
    indicator = st.selectbox("📉 Technical Indicator", ['RSI', 'MACD', 'Moving Average'] if chart_type == 'Line' else ['RSI', 'MACD'])

# -------------------- Charts --------------------
ticker_obj = yf.Ticker(ticker)
data_full = ticker_obj.history(period="max")
data_full = data_full.reset_index()

if chart_type == 'Candle':
    st.plotly_chart(candlestick(data_full, selected_period), use_container_width=True)
    if indicator == 'RSI':
        st.plotly_chart(RSI(data_full, selected_period), use_container_width=True)
    elif indicator == 'MACD':
        st.plotly_chart(MACD(data_full, selected_period), use_container_width=True)
else:
    st.plotly_chart(close_chart(data_full, selected_period), use_container_width=True)
    if indicator == 'RSI':
        st.plotly_chart(RSI(data_full, selected_period), use_container_width=True)
    elif indicator == 'MACD':
        st.plotly_chart(MACD(data_full, selected_period), use_container_width=True)
    elif indicator == 'Moving Average':
        st.plotly_chart(Moving_average(data_full, selected_period), use_container_width=True)
