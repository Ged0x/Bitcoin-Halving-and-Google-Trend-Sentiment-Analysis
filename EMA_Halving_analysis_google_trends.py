import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

ticker = 'BTC-USD'
smooth = 17

# Downloading data
asset_data = yf.download(ticker, start="2015-12-01", progress=False)['Adj Close']

# Calculating EMA
EMA_asset_data = pd.Series(dtype='float64', index=asset_data.index)

for i in range(len(asset_data)):
    if i == 0:
        EMA_asset_data[i] = asset_data[i]
    else:
        EMA_asset_data[i] = (asset_data[i] * (smooth/(1+i))) + (EMA_asset_data[i-1] * (1-(smooth/(1+i))))

# Marking halving dates
halving_dates = {
    'November 8, 2012': '2012-11-28',
    'July 9, 2016': '2016-07-09',
    'May 11, 2020': '2020-05-11',
    'April 19, 2024': '2024-04-19'
}

# Convert halving dates to datetime objects
halving_dates = {date: pd.to_datetime(date_index) for date, date_index in halving_dates.items() if date_index in EMA_asset_data.index}

# Extend EMA_asset_data to before April 19, 2024
end_date = pd.to_datetime('2024-04-18')
EMA_asset_data = EMA_asset_data.reindex(pd.date_range(start=EMA_asset_data.index[0], end=end_date, freq='D'))

# Plotting
plt.figure(figsize=(10, 5))
plt.plot(asset_data, label='Asset Data')
plt.plot(EMA_asset_data, label='EMA')

for date, date_index in halving_dates.items():
    plt.axvline(x=date_index, color='r', linestyle='--', label='Halving')
    plt.text(date_index, EMA_asset_data.loc[date_index], date, rotation=90, verticalalignment='bottom')

# Adding vertical line for April 18, 2024
plt.axvline(x=pd.to_datetime('2024-04-18'), color='g', linestyle='--', label='April 18, 2024')
plt.text(pd.to_datetime('2024-04-18'), EMA_asset_data.loc['2024-04-18'], 'April 18, 2024', rotation=90, verticalalignment='bottom')

plt.title('Asset Data vs Exponential Moving Average (EMA)')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()
