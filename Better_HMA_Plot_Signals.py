import schedule
import time
import numpy as np
import yfinance as yf
import pandas as pd
import math
import plotly.graph_objects as go

#ticker = input('What ticker do you want?: ')
ticker = 'SPY'
#fname = input('What is the name of the yahoo file?')
fname = 'yahoo.csv'
#px_history = input('How far back for the historical price data?: ')
px_history = '5y'
#fname1 = input('What is the name of the output file?')
fname1 = 'betterHMA.csv'
#window_inp = input("How many periods for the gooseline?: ")
window_inp = int(6)
#tail_inp = input('How many data points should print out?: ')
#tail_int = int(tail_inp)
tail_int = int(25)

    # input questions

data = yf.download(ticker, period = px_history)
#print(data)

data.to_csv(fname)
df = pd.read_csv(fname)
num_periods = int(window_inp)
df['sma_indicator'] = df['Close'].rolling(num_periods).mean()

# WMA
weights = np.arange(1, (num_periods + 1))  # this creates an array with integers 1 to num_periods included
# df['weights'] = pd.Series(weights_list)

# wma_indicator = numbers_series.rolling(num_periods).apply(lambda prices: np.dot(prices, weights)/weights.sum(), raw=True)

wma = df['Close'].rolling(num_periods).apply(lambda prices: np.dot(prices, weights) / weights.sum(), raw=True)
df['wma_indicator'] = pd.Series(wma)

# take the slope which is the difference between each number using the Numpy diff function
x = np.diff(df['sma_indicator'])
# y = np.diff(df['ema_indicator'])
z = np.diff(df['wma_indicator'])

# pass the variable into a series so that it can print the output into the dataframe even though it has
# number of outputs than the other variables
df['diff_sma'] = pd.Series(x)
# df['diff_ema'] = pd.Series(y)
df['diff_wma'] = pd.Series(z)

# buy/sell toggle switch
df['SMA_Buy_Trigger'] = np.where(df['diff_sma'] > 0, "Long", "Short")
# df['Buy_Trigger'] = np.where(df['diff_ema']>0,"Long","Short")
df['WMA_Buy_Trigger'] = np.where(df['diff_wma'] > 0, "Long", "Short")

# Guts of WTD formula

betterhma_length = num_periods
betterhma_length_half = int(betterhma_length / 2)
# avg_wtd = wma_indicator
df['ema_of_wma'] = df['wma_indicator'].ewm(span=betterhma_length_half, adjust=False).mean()
df['two_ema_of_wma'] = 2 * df['ema_of_wma']
df['firstpart_ema'] = df['two_ema_of_wma']

sqr_betterhma_length = int(math.sqrt(betterhma_length))
df['secondpart_ema'] = df['wma_indicator'].ewm(span=sqr_betterhma_length, adjust=False).mean()
df['betterhma'] = df['firstpart_ema'] - df['secondpart_ema']

# Toggle Switch
w = np.diff(df['betterhma'])
df['diff_betterhma'] = pd.Series(w)
df['Buy_BetterHMA'] = np.where(df['diff_betterhma'] > 0, "Long", "Short")
df['Buy_Better'] = np.where(df['diff_betterhma'] > 0, 1, 0)  # Buy = 1 Sell = 0


#fname1 = 'wtd3.csv'

dfobj = df[['Date', 'Close', 'betterhma','Buy_BetterHMA']].tail(tail_int)

dfobj.to_csv(fname1)

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=df['Date'],
        y=df['betterhma'],
        name="HMA"
    ))

fig.add_trace(
    go.Scatter(
        x=df['Date'],
        y=df['Close'],
        name="Price"
    ))

fig.show()
print(dfobj)
