import datetime

import index
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_ta as ta

stock = input("Enter Stock Name ")
capital = input("Enter Capital")

sql: str = "select Date ,close from Indexes where IndexID = 3 order by ID DESC"
close_data_index = pd.read_sql_query(sql, index.conn)
# sql: str = "select Date ,close from Indexes where IndexID = 5 order by ID DESC"
# close_data_stock = pd.read_sql_query(sql, index.conn)
# create 20 days simple moving average column

# returns = close_data_index['CLOSE'].apply(lambda x: np.log(x/x.shift(1)))
print(close_data_index['CLOSE'].skew())
close_data_index['20_SMA'] = close_data_index['CLOSE'].rolling(window=20).mean()
# create 50 days simple moving average column
close_data_index['50_SMA'] = close_data_index['CLOSE'].rolling(window=50).mean()
# create 200 days simple moving average column
close_data_index['200_SMA'] = close_data_index['CLOSE'].rolling(window=200).mean()
std = close_data_index['CLOSE'].rolling(20).std()  # <-- Get rolling standard deviation for 20 days
close_data_index['bollinger_up'] = close_data_index['20_SMA'] + std * 2  # Calculate top band
close_data_index['bollinger_down'] = close_data_index['20_SMA'] - std * 2  # Calculate bottom band
close_data_index['Signal'] = 0.0
close_data_index['Signal'] = np.where(close_data_index['20_SMA'] > close_data_index['50_SMA'], 1.0, 0.0)
close_data_index['Position'] = close_data_index['Signal'].diff()
# print(len(close_data))
close_data_index.DATE = pd.to_datetime(close_data_index['DATE'])

close_data_index = close_data_index.set_index('DATE')
close_data_index = close_data_index.tail(500)
# plt.plot(close_data_index.index, close_data_index['CLOSE'], color='g', marker='+', label='Closing Prices', )
plt.plot(close_data_index.index, close_data_index['20_SMA'], color='r', label='20-day SMA')
plt.plot(close_data_index.index, close_data_index['50_SMA'], color='m', label='50-day SMA')
plt.plot(close_data_index.index, close_data_index['200_SMA'], color='y', label='200-day SMA')
plt.plot(close_data_index.index, close_data_index['bollinger_up'], color='c', label='BB')
plt.plot(close_data_index.index, close_data_index['bollinger_down'], color='c')
# plt.figure(figsize=(20, 10))
# plot close price, short-term and long-term moving averages
# plot ‘buy’ signals
plt.plot(close_data_index[close_data_index['Position'] == 1].index,
         close_data_index['20_SMA'][close_data_index['Position'] == 1], '^', markersize=10, color='g', label='buy')
# plot ‘sell’ signals
plt.plot(close_data_index[close_data_index['Position'] == -1].index,
         close_data_index['50_SMA'][close_data_index['Position'] == -1], 'v', markersize=10, color='r', label='sell')

plt.xlabel('Date', fontsize=5)
plt.title(f'{stock} Market Analysis', fontsize=15)
plt.xticks(rotation=45)
plt.legend()
plt.grid()
plt.show()
#plt.close()

buySignal = close_data_index[close_data_index['Position'] == 1]
sellSignal = close_data_index[close_data_index['Position'] == -1]
if buySignal.index[-1] > sellSignal.index[-1]:
    date = buySignal.index[-1]
    price = buySignal['CLOSE'].iloc[-1]
else:
    date = sellSignal.index[-1]
    price = sellSignal['CLOSE'].iloc[-1]

shares = float(capital) // float(price)
p_or_l= (shares*close_data_index['CLOSE'].iloc[-1])-(shares*price)
data = [[stock, 'S&P 500', shares, close_data_index['CLOSE'].skew(), close_data_index['CLOSE'].kurt(), date,p_or_l ]]
print(pd.DataFrame(data, columns=["Stock", "Index", "Shares", "Skew", "Kurtosis", "Trigger on ", "Profit/loss Today"]))
