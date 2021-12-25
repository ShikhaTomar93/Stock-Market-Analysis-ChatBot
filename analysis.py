import initialize
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

stock = input("Enter Stock Name ")
capital = input("Enter Capital")

sql: str = f"SELECT DATE, CLOSE FROM Stock_Price sp JOIN Stocks s ON sp.Stock_ID = s.Stock_ID WHERE s.Stock_Symbol = '{stock}'"
stock_data = pd.read_sql_query(sql, initialize.conn)
# sql: str = "select Date ,close from Indexes where IndexID = 5 order by ID DESC"
# close_data_stock = pd.read_sql_query(sql, index.conn)
# create 20 days simple moving average column

# returns = close_data_index['CLOSE'].apply(lambda x: np.log(x/x.shift(1)))
print(stock_data['CLOSE'].skew())
stock_data['20_SMA'] = stock_data['CLOSE'].rolling(window=20).mean()
# create 50 days simple moving average column
stock_data['50_SMA'] = stock_data['CLOSE'].rolling(window=50).mean()
# create 200 days simple moving average column
stock_data['200_SMA'] = stock_data['CLOSE'].rolling(window=200).mean()
std = stock_data['CLOSE'].rolling(20).std()  # <-- Get rolling standard deviation for 20 days
stock_data['bollinger_up'] = stock_data['20_SMA'] + std * 2  # Calculate top band
stock_data['bollinger_down'] = stock_data['20_SMA'] - std * 2  # Calculate bottom band
stock_data['Signal'] = 0.0
stock_data['Signal'] = np.where(stock_data['20_SMA'] > stock_data['50_SMA'], 1.0, 0.0)
stock_data['Position'] = stock_data['Signal'].diff()
# print(len(close_data))
stock_data.DATE = pd.to_datetime(stock_data['DATE'])

stock_data = stock_data.set_index('DATE')
stock_data = stock_data.tail(500)
# plt.plot(close_data_index.index, close_data_index['CLOSE'], color='g', marker='+', label='Closing Prices', )
plt.plot(stock_data.index, stock_data['20_SMA'], color='r', label='20-day SMA')
plt.plot(stock_data.index, stock_data['50_SMA'], color='m', label='50-day SMA')
plt.plot(stock_data.index, stock_data['200_SMA'], color='y', label='200-day SMA')
plt.plot(stock_data.index, stock_data['bollinger_up'], color='c', label='BB')
plt.plot(stock_data.index, stock_data['bollinger_down'], color='c')
# plt.figure(figsize=(20, 10))
# plot close price, short-term and long-term moving averages
# plot ‘buy’ signals
plt.plot(stock_data[stock_data['Position'] == 1].index,
         stock_data['20_SMA'][stock_data['Position'] == 1], '^', markersize=10, color='g', label='buy')
# plot ‘sell’ signals
plt.plot(stock_data[stock_data['Position'] == -1].index,
         stock_data['50_SMA'][stock_data['Position'] == -1], 'v', markersize=10, color='r', label='sell')

plt.xlabel('Date', fontsize=5)
plt.title(f'{stock} Market Analysis', fontsize=15)
plt.xticks(rotation=45)
plt.legend()
plt.grid()
plt.show()
#plt.close()

buySignal = stock_data[stock_data['Position'] == 1]
sellSignal = stock_data[stock_data['Position'] == -1]
if buySignal.index[-1] > sellSignal.index[-1]:
    date = buySignal.index[-1]
    price = buySignal['CLOSE'].iloc[-1]
else:
    date = sellSignal.index[-1]
    price = sellSignal['CLOSE'].iloc[-1]

shares = float(capital) // float(price)
p_or_l= (shares * stock_data['CLOSE'].iloc[-1]) - (shares * price)
data = [[stock, 'S&P 500', shares, stock_data['CLOSE'].skew(), stock_data['CLOSE'].kurt(), date, p_or_l]]
print(pd.DataFrame(data, columns=["Stock", "Index", "Shares", "Skew", "Kurtosis", "Trigger on ", "Profit/loss Today"]))
