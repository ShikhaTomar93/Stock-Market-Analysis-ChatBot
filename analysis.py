import index
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_ta as ta

sql: str = "select Date ,close from Indexes where IndexID = 5 order by ID DESC"
close_data = pd.read_sql_query(sql, index.conn)
print(close_data.head())
# create 20 days simple moving average column
close_data['20_SMA'] = close_data['CLOSE'].rolling(window=20).mean()
# create 50 days simple moving average column
close_data['50_SMA'] = close_data['CLOSE'].rolling(window=50).mean()
# create 200 days simple moving average column
close_data['200_SMA'] = close_data['CLOSE'].rolling(window=200).mean()
# close_data['Signal'] = 0.0
# close_data['Signal'] = np.where(close_data['50_SMA'] > close_data['200_SMA'], 1.0, 0.0)
# close_data['Position'] = close_data['Signal'].diff()
# print(len(close_data))
close_data.DATE = pd.to_datetime(close_data['DATE'])
print(close_data.tail())
close_data = close_data.set_index('DATE')
display_data = close_data.tail(500)
plt.plot(display_data.index, display_data['CLOSE'], color='g', marker='+', label='Closing Prices', )
plt.plot(display_data.index, display_data['20_SMA'], color='r', label='20-day SMA')
plt.plot(display_data.index, display_data['50_SMA'], color='m', label='50-day SMA')
plt.plot(display_data.index, display_data['200_SMA'], color='y', label='200-day SMA')
# plt.figure(figsize=(20, 10))
# plot close price, short-term and long-term moving averages
# plot ‘buy’ signals
# plt.plot(close_data[close_data['Position'] == 1].index,close_data['50_SMA'][close_data['Position'] == 1],'^', markersize=15, color='g', label='buy')
# plot ‘sell’ signals
# plt.plot(close_data[close_data['Position'] == -1].index,close_data['200_SMA'][close_data['Position'] == -1],'v', markersize=15, color='r', label='sell')
plt.ylabel('Price', fontsize=5)
plt.xlabel('Date', fontsize=5)
plt.title('Stock Market Analysis', fontsize=20)
plt.xticks(rotation=45)
plt.legend()
plt.grid()
plt.show()
