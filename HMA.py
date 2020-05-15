import yfinance as yf
import numpy as np

# download dataframe
#    # use "period" instead of start/end
#         # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
# fetch data by interval (including intraday if period < 60 days)
# valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo

#df = yf.download("SPY AMZN", period='1mo', interval = '5m', group_by= 'ticker')
df = yf.download("TSLA", period='1mo', interval = '5m',group_by='ticker')

#print(df)
num_periods = 9
df['hma_indicator'] = df['Close'].rolling(num_periods).mean()
#print(df)
df['previous_value'] = df["hma_indicator"].shift(1)
#print(df)
df['difference'] = df['hma_indicator'] - df['previous_value']
#print(df)
df['long_short_signal'] = np.where(df['difference'] > 0, 'long', 'short')
group_by = 'ticker'
print(df)
#df.to_csv('yahoo_long_short_signal1.csv')
df.to_csv('file1.csv')