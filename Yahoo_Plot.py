# The point of this code is to: 1. Pull data from Yahoo Finance 2. Process that data into an sma
# 3. Plot the sma against the price.

import yfinance as yf
import numpy as np
import plotly.graph_objects as go
import pandas as pd

# download dataframe
#    # use "period" instead of start/end
#         # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
# fetch data by interval (including intraday if period < 60 days)
# valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo

#df = yf.download("SPY AMZN", period='1mo', interval = '5m', group_by= 'ticker')
#called on the data in Yahoo Finance and put it in dataframe and then pushed into a .csv/excel file
data = yf.download("SPY", period='1y')
print(data)
fname = 'yahoo_plot.csv'
data.to_csv(fname)
df = pd.read_csv(fname)

#used the historical data to calculate a sma (simple moving average)
#print(df)
num_periods = 9
df['sma_indicator'] = df['Close'].rolling(num_periods).mean()

num_period_one = 21
df['sma_indicator_one'] = df['Close'].rolling(num_period_one).mean()


#plot the sma against price

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=df['Date'],
        y=df['sma_indicator'],
        name="SMA"
    ))

fig.add_trace(
    go.Scatter(
        x=df['Date'],
        y=df['sma_indicator_one'],
        name="SMA_1"
    ))


fig.add_trace(
    go.Scatter(
        x=df['Date'],
        y=df['Close'],
        name="Price"
    ))

fig.show()
