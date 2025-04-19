import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go

# ---------------- Page Config ----------------
st.set_page_config(page_title="Trade Alert", page_icon="🚨", layout="wide")

# ---------------- Page Styling ----------------
st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
            background-color: #f4f7fa;
        }
        .stSidebar {
            background-color: #b2d8c2 !important;
            background-image: linear-gradient(to bottom, #b2d8c2, #9acaa6);
        }
    </style>
""", unsafe_allow_html=True)

st.title("🚨 Trade Alert")
st.markdown("Detect spikes and dips in stock prices using Z-score-based anomaly detection.")

# ---------------- Ticker Input ----------------
popular_tickers = {
    "Apple (AAPL)": "AAPL", "Tesla (TSLA)": "TSLA", "Microsoft (MSFT)": "MSFT",
    "Amazon (AMZN)": "AMZN", "Google (GOOGL)": "GOOGL", "Meta (META)": "META", "NVIDIA (NVDA)": "NVDA"
}

col1, col2 = st.columns(2)
today = datetime.date.today()

with col1:
    ticker_dropdown = st.selectbox("📂 Choose Stock", list(popular_tickers.keys()))
    custom_ticker = st.text_input(" Or enter custom ticker", "")
    ticker = custom_ticker.strip().upper() if custom_ticker else popular_tickers[ticker_dropdown]

with col2:
    start_date = st.date_input("📅 Start Date", datetime.date(today.year - 1, today.month, today.day))
    end_date = st.date_input("📅 End Date", today)

# ---------------- Data & Analysis ----------------
try:
    df = yf.download(ticker, start=start_date, end=end_date)[['Close']].dropna()

    df['RollingMean'] = df['Close'].rolling(20).mean()
    df['RollingStd'] = df['Close'].rolling(20).std()
    df.dropna(inplace=True)

    df['Zscore'] = ((df['Close'].squeeze() - df['RollingMean'].squeeze()) / df['RollingStd'].squeeze())
    df['Anomaly'] = df['Zscore'].apply(lambda x: '📈 Spike' if x > 2 else ('📉 Dip' if x < -2 else 'Normal'))
    anomalies = df[df['Anomaly'] != 'Normal']

    # ---------------- Summary Stats ----------------
    st.markdown("### 🔎 Insight Highlights")
    col1, col2, col3 = st.columns(3)
    col1.metric("📈 Spikes", len(anomalies[anomalies['Anomaly'] == '📈 Spike']))
    col2.metric(" 📉 Dips", len(anomalies[anomalies['Anomaly'] == '📉 Dip']))
    col3.metric("📅 Days Analyzed", len(df))

    # ---------------- Z-Score Line Chart ----------------
    st.markdown("### 🚦 Anomaly Signal Tracker (Z-Score Thresholds)")
    z_fig = go.Figure()
    z_fig.add_trace(go.Scatter(x=df.index, y=df['Zscore'], mode='lines', name='Z-Score', line=dict(color='orange')))
    z_fig.add_hline(y=2, line=dict(color='limegreen', dash='dash'), annotation_text='Spike Threshold')
    z_fig.add_hline(y=-2, line=dict(color='red', dash='dash'), annotation_text='Dip Threshold')
    z_fig.update_layout(
        plot_bgcolor='#1e1e1e', paper_bgcolor='#1e1e1e',
        font=dict(color='white'), height=400,
        xaxis=dict(gridcolor='#444'), yaxis=dict(gridcolor='#444')
    )
    st.plotly_chart(z_fig, use_container_width=True)

    # ---------------- Insight Summary ----------------
    st.markdown("### ⚡ Quick Interpretation")

    if not anomalies.empty:
        latest = anomalies.iloc[-1]
        latest_date = anomalies.index[-1].strftime('%B %d, %Y')  # properly formatted date string
        z = float(latest['Zscore'])
        price = float(latest['Close'])
        anomaly_type = latest['Anomaly']
        anomaly_word = "Spike 📈" if "Spike" in anomaly_type else "Dip 📉"

        # 🔄 Dynamic explanation logic
        if abs(z) < 2.5:
            explanation = "a mild deviation, possibly due to regular price fluctuation."
        elif abs(z) < 3:
            explanation = "a moderate shift, likely driven by short-term volatility or sentiment."
        else:
            explanation = "an extreme deviation, possibly triggered by breaking news or market shock."

        direction = "upward momentum 📈" if z > 0 else "a price drop 📉"

        st.markdown(f"""
        On **{latest_date}**, the stock **{ticker}** experienced a **{anomaly_word}**,  
        with a Z-score of **{z:.2f}** and a closing price of **${price:.2f}**.

        This reflects **{direction}**, with **{explanation}**  
        The price deviated significantly from its 20-day moving average.
        """)
    else:
        st.success("✅ No significant spikes or dips detected during the selected time period.")

    # ---------------- Expanders ----------------
    with st.expander("📄 View Anomalies Table"):
        table = anomalies.copy()
        table.index = table.index.strftime('%Y-%m-%d')
        st.dataframe(table[['Close', 'Zscore', 'Anomaly']].rename(
            columns={'Close': 'Close Price', 'Zscore': 'Z-Score'}).round(2), use_container_width=True)

    with st.expander("🕒 View Timeline of Anomalies"):
        emoji = df['Anomaly'].map({'📈 Spike': '📈', '📉 Dip': '📉', 'Normal': '⚪'})
        t_fig = go.Figure()
        t_fig.add_trace(go.Scatter(
            x=df.index, y=[0]*len(df), mode='text', text=emoji,
            textfont=dict(size=16), hovertext=df['Anomaly'], hoverinfo='text'
        ))
        t_fig.update_layout(
            height=100, yaxis=dict(visible=False), xaxis=dict(showgrid=False),
            plot_bgcolor='white', paper_bgcolor='white', margin=dict(t=20, b=30)
        )
        st.plotly_chart(t_fig, use_container_width=True)

except Exception as e:
    st.error(f"❌ Error: {e}")
