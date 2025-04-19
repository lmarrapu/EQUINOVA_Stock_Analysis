import plotly.graph_objects as go
import pandas as pd
import dateutil.relativedelta as relativedelta
import ta
import datetime

def plotly_table(dataframe):
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["<b>Metric</b>"] + ["<b>" + str(col) + "</b>" for col in dataframe.columns],
            fill_color='#9acaa6',  # Sidebar green tone
            align='center',
            font=dict(color='white', size=14, family='Times New Roman'),
            height=38
        ),
        cells=dict(
            values=[dataframe.index] + [dataframe[col] for col in dataframe.columns],
            fill_color='white',
            align='left',
            line_color='#DDDDDD',
            font=dict(color="#111", size=13, family='Times New Roman')
        )
    )])

    fig.update_layout(
        height=350,
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    return fig

def filter_data(dataframe, num_period):
    if 'Date' not in dataframe.columns:
        dataframe = dataframe.reset_index()

    if num_period == '1mo':
        date = dataframe['Date'].iloc[-1] + relativedelta.relativedelta(months=-1)
    elif num_period == '5d':
        date = dataframe['Date'].iloc[-1] + relativedelta.relativedelta(days=-5)
    elif num_period == '6mo':
        date = dataframe['Date'].iloc[-1] + relativedelta.relativedelta(months=-6)
    elif num_period == '1y':
        date = dataframe['Date'].iloc[-1] + relativedelta.relativedelta(years=-1)
    elif num_period == '5y':
        date = dataframe['Date'].iloc[-1] + relativedelta.relativedelta(years=-5)
    else:
        date = dataframe['Date'].iloc[0]

    return dataframe[dataframe['Date'] > date]

def close_chart(dataframe, num_period=False):
    if num_period:
        dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'],
                             mode='lines', name='Open',
                             line=dict(width=2, color='#1E90FF')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'],
                             mode='lines', name='Close',
                             line=dict(width=2, color='Pink')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'],
                             mode='lines', name='High',
                             line=dict(width=2, color='#FF8C00')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'],
                             mode='lines', name='Low',
                             line=dict(width=2, color='#DC143C')))
    fig.update_layout(height=500, plot_bgcolor='#1e1e1e', paper_bgcolor='#1e1e1e',
                      font=dict(color='white', family='Times New Roman', size=13),
                      legend=dict(yanchor="top", xanchor="right", font=dict(color='white')),
                      xaxis=dict(rangeslider_visible=True, gridcolor='#444'),
                      yaxis=dict(gridcolor='#444'))
    return fig

def candlestick(dataframe, num_period):
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure(data=[
        go.Candlestick(
            x=dataframe['Date'],
            open=dataframe['Open'],
            high=dataframe['High'],
            low=dataframe['Low'],
            close=dataframe['Close'],
            increasing_line_color='#4CAF50',
            decreasing_line_color='#FF7043',
            line_width=2
        )
    ])
    fig.update_layout(title="📊 Candlestick Chart",
                      font=dict(family='Times New Roman', size=13, color='white'),
                      plot_bgcolor='#1e1e1e', paper_bgcolor='#1e1e1e',
                      xaxis=dict(rangeslider_visible=True, gridcolor="#333", tickfont=dict(color='white')),
                      yaxis=dict(gridcolor="#333", tickfont=dict(color='white')),
                      legend=dict(font=dict(color='white'), bgcolor='#2a2a2a', bordercolor='white', borderwidth=1),
                      title_font=dict(color='white'), height=500)
    return fig

def RSI(dataframe, num_period):
    dataframe['RSI'] = ta.momentum.RSIIndicator(dataframe['Close']).rsi()
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['RSI'],
                             mode='lines', name='RSI', line=dict(width=2, color='#00BFFF')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=[70]*len(dataframe),
                             mode='lines', name='Overbought', line=dict(dash='dash', color='red')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=[30]*len(dataframe),
                             mode='lines', name='Oversold', line=dict(dash='dash', color='lime')))
    fig.update_layout(height=250, plot_bgcolor='#1e1e1e', paper_bgcolor='#1e1e1e',
                      font=dict(color='white', family='Times New Roman', size=13),
                      xaxis=dict(gridcolor="#333", tickfont=dict(color='white')),
                      yaxis=dict(gridcolor="#333", tickfont=dict(color='white')),
                      legend=dict(orientation="h", font=dict(color='white'), bgcolor='#2a2a2a', bordercolor='white', borderwidth=1))
    return fig

def Moving_average(dataframe, num_period):
    dataframe['SMA_50'] = ta.trend.SMAIndicator(dataframe['Close'], 50).sma_indicator()
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'],
                             mode='lines', name='Close', line=dict(width=2, color='white')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['SMA_50'],
                             mode='lines', name='SMA_50', line=dict(width=2, color='orange')))
    fig.update_layout(height=500, plot_bgcolor='#1e1e1e', paper_bgcolor='#1e1e1e',
                      font=dict(color='white', family='Times New Roman', size=13),
                      legend=dict(yanchor="top", xanchor="right", font=dict(color='white'), bgcolor='#2a2a2a', bordercolor='white', borderwidth=1),
                      xaxis=dict(rangeslider_visible=True, gridcolor='#444'),
                      yaxis=dict(gridcolor='#444'))
    return fig

def MACD(dataframe, num_period):
    macd_indicator = ta.trend.MACD(dataframe['Close'])
    dataframe['MACD'] = macd_indicator.macd()
    dataframe['Signal'] = macd_indicator.macd_signal()
    dataframe['Histogram'] = macd_indicator.macd_diff()
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['MACD'],
                             mode='lines', name='MACD', line=dict(width=2, color='#FFBF00')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Signal'],
                             mode='lines', name='Signal', line=dict(width=2, color='#00CED1', dash='dash')))
    fig.add_trace(go.Bar(x=dataframe['Date'], y=dataframe['Histogram'], name='Histogram',
                         marker_color=['#00FA9A' if val >= 0 else '#FF4500' for val in dataframe['Histogram']]))
    fig.update_layout(height=250, plot_bgcolor='#1e1e1e', paper_bgcolor='#1e1e1e',
                      font=dict(color='white', family='Times New Roman', size=13),
                      xaxis=dict(gridcolor="#333", tickfont=dict(color='white')),
                      yaxis=dict(gridcolor="#333", tickfont=dict(color='white')),
                      legend=dict(orientation="h", font=dict(color='white'), bgcolor='#2a2a2a', bordercolor='white', borderwidth=1))
    return fig

def Moving_average_forecast(forecast):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=forecast.index[:-30], y=forecast['Close'].iloc[:-30],
                             mode='lines', name='Historical Close', line=dict(width=2, color='white')))
    fig.add_trace(go.Scatter(x=forecast.index[-30:], y=forecast['Close'].iloc[-30:],
                             mode='lines', name='Forecasted Close', line=dict(width=2, color='deepskyblue')))
    fig.update_layout(height=500, plot_bgcolor='#1e1e1e', paper_bgcolor='#1e1e1e',
                      font=dict(color='white', family='Times New Roman', size=13),
                      xaxis=dict(rangeslider_visible=True, gridcolor='#444'),
                      yaxis=dict(gridcolor='#444'),
                      legend=dict(yanchor="top", xanchor="right", font=dict(color='white'), bgcolor='#2a2a2a', bordercolor='white', borderwidth=1))
    return fig
