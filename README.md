# 📊 EquiNova: Smart Trading Analytics Platform

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://equinovastockanalysis-mywkt7xwpcqhfhyjjj.streamlit.app/)

## 🔍 Overview

**EquiNova** is a powerful, interactive stock analytics and forecasting web application that merges real-time market data with advanced statistical modeling. Built using Streamlit and powered by live Yahoo Finance data, this platform offers traders and investors a comprehensive toolkit for making data-driven decisions.

The application transforms complex financial data into actionable insights through dynamic visualizations, AI-powered forecasting, and intuitive anomaly detection - all within a clean, user-friendly interface.

> 🌐 **[Live Demo](https://equinovastockanalysis-mywkt7xwpcqhfycgfhyjjj.streamlit.app/)**

## ✨ Key Features

### 📈 Market Pulse
- **Real-time stock analysis** with detailed company information
- **Technical indicators** including RSI, MACD, and Moving Averages
- **Financial metrics** visualization with interactive charts
- **Historical performance** analysis with customizable date ranges

### 🔮 Price Forecast
- **30-day closing price prediction** using advanced ARIMA time series modeling
- **Statistical accuracy metrics** (RMSE evaluation) for forecast reliability
- **Trend identification** with confidence intervals
- **Model performance visualization** with actual vs. predicted comparisons

### 🚨 Trade Alert
- **Automated anomaly detection** using sophisticated Z-score analysis
- **Market spike and dip identification** with clear visual markers
- **Emoji-based anomaly timelines** for quick pattern recognition
- **Custom alert thresholds** for personalized trading strategies

### 💹 Live Market Overview
- **Real-time index tracking** for S&P 500, NASDAQ and DOW JONES
- **Trend visualization** with dynamic markers and color coding
- **At-a-glance market sentiment** indicators
- **Responsive updates** reflecting current market conditions

## 🛠️ Tech Stack

- **Frontend/UI**: Streamlit, HTML/CSS, PIL
- **Data Processing**: yfinance, pandas, numpy
- **Statistical Modeling**: statsmodels (ARIMA), Z-score analysis, StandardScaler
- **Data Visualization**: Plotly (interactive candlestick charts, line charts, tables, timelines)
- **Development Environment**: VS Code

## 🧮 Forecasting Methodology

EquiNova employs **ARIMA (AutoRegressive Integrated Moving Average)** modeling to deliver accurate price forecasts:

1. Time series transformation to achieve stationarity
2. Parameter optimization through grid search
3. Forward prediction with confidence intervals
4. Performance evaluation using RMSE and relative error metrics
5. Inverse scaling for intuitive price representation

Our dynamic approach to time series analysis ensures adaptability to changing market conditions while maintaining forecast reliability.


### ⭐️ **If you find this repository useful, give it a star!**
