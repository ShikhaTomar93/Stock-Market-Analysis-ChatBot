import sqlite3
import os
from sqlite3 import Error
import pandas as pd
import numpy as np

def create_connection(db_file, delete_db=False):
    if delete_db and os.path.exists(db_file):
        os.remove(db_file)

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("PRAGMA foreign_keys = 1")
    except Error as e:
        print(e)

    return conn


def create_table(create_table_sql, drop_table_name=None):
    if drop_table_name:  # You can optionally pass drop_table_name to drop the table.
        try:
            c = conn.cursor()
            c.execute("""DROP TABLE IF EXISTS %s""" % (drop_table_name))
        except Error as e:
            print(e)

    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def execute_sql_statement(sql_statement):
    cur.execute(sql_statement)
    rows = cur.fetchall()

    return rows

conn = create_connection("stockMarket.db", delete_db=False)
cur = conn.cursor()
def initialize_database():
    # table to store general info on indexes
    sql_statement = """
            CREATE TABLE Indexes 
                (Index_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 Index_Symbol TEXT NOT NULL,
                 Index_Name TEXT NOT NULL 
                );"""
    create_table(sql_statement, 'Indexes')
    # table to store price data for indexes
    sql_statement = """
            CREATE TABLE Index_Price 
                (Index_ID INTEGER, 
                 Date TEXT,
                 Open REAL,
                 High REAL,
                 Low REAL,
                 Close REAL,
                 Volume REAL,
                 FOREIGN KEY(Index_ID) REFERENCES Indexes(Index_ID)             
                );"""
    create_table(sql_statement, 'Index_Price')
    # creating table for general info on the stocks
    sql_statement = """
            CREATE TABLE Stocks 
                (Stock_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 Stock_Symbol TEXT NOT NULL,
                 Stock_Name TEXT NOT NULL,
                 Sector TEXT NOT NULL,
                 UNIQUE(Stock_Symbol)
                );"""
    create_table(sql_statement, 'Stocks')
    # creating table for general info on the stocks
    sql_statement = """
            CREATE TABLE Stock_Index 
                (Stock_ID INTEGER NOT NULL,
                 Index_ID INTEGER NOT NULL,
                 Weight INTEGER NOT NULL,
                 FOREIGN KEY(Index_ID) REFERENCES Indexes(Index_ID),
                 FOREIGN KEY(Stock_ID) REFERENCES Stocks(Stock_ID) 
                );"""
    create_table(sql_statement, 'Stock_Index')
    # creating table for the prices of all the stocks
    sql_statement = """
            CREATE TABLE Stock_Price 
                (Stock_ID INTEGER, 
                 Date REAL,
                 Open REAL,
                 High REAL,
                 Low REAL,
                 Close REAL,
                 Volume REAL,
                 FOREIGN KEY(Stock_ID) REFERENCES Stocks(Stock_ID)          
                );"""
    create_table(sql_statement, 'Stock_Price')


# inserting index and stocks data in the table
def insert_index_info():
    index_data = [('IXIC', 'Nasdaq Composite'), ('DJIA', 'Dow Jones Industrial Average'),
                  ('NDX', 'Nasdaq 100'), ('RUT', 'Russell 2000'), ('SPX', 'S&P 500')]
    cur.executemany(f"INSERT INTO Indexes(Index_Symbol, Index_Name) VALUES(?,?);", index_data)
    conn.commit()

# inserting index prices and stocks prices in the table
def insert_data(tablename, tableCol, df):
    values_count = ','.join(['?'] * len(tableCol))
    data_list = df.values.tolist()
    data_splitted = np.array_split(data_list, 3) #SQLite does not support bulk insertion of more than 1000 rows
    for data in data_splitted:
        cur.executemany(f"INSERT OR IGNORE INTO {tablename}{tableCol} VALUES ({values_count});", data)
        conn.commit()
    del df

def get_data_from_table(col_name, compare_col, compare_data, table_name):
    row = execute_sql_statement(f"select {col_name} from {table_name} where {compare_col} in {tuple(compare_data)}")
    return row

def get_dataframe_index(filename):
    file_type = filename.split('.')[1]
    if file_type == 'csv':
        df = pd.read_csv(filename)
        index_ID = filename.split('_')[1][:-4]
    else:
        df = pd.read_excel(filename)
        index_ID = filename.split('_')[1][:-5]
    return df, index_ID

def get_dataframe_stock(filename):
    df = pd.read_csv(filename)
    index_ID = filename.split('/')[2][:-4]
    return df, index_ID

def insert_stock_info():
    table_col_stock = ('Stock_Symbol', 'Stock_Name', 'Sector')
    table_col_stock_index = ('Stock_ID', 'Index_ID', 'Weight')
    datasets = ['datasets/Holdings_DJIA.xlsx', 'datasets/Holdings_NDX.csv', 'datasets/Holdings_RUT.csv',
                'datasets/Holdings_SPX.xlsx','datasets/Holdings_IXIC.xlsx']
    for filename in datasets:
        df, index_symbol = get_dataframe_index(filename)
        index_symbol = index_symbol.split()
        index_symbol.append('')
        df.rename(columns={"Ticker": "Stock_Symbol", "Name": "Stock_Name"}, inplace=True)
        df_stock = df[list(table_col_stock)]
        insert_data('Stocks', table_col_stock, df_stock)

        row = get_data_from_table('Index_ID', 'Index_Symbol', index_symbol, 'Indexes')
        df['Index_ID'] = row[0][0]
        stock_symbol = df['Stock_Symbol'].tolist()
        row = get_data_from_table('Stock_ID', 'Stock_Symbol', stock_symbol, 'Stocks')
        df['Stock_ID'] = pd.DataFrame(row)
        df_stock_index = df[['Stock_ID', 'Index_ID', 'Weight']]
        insert_data('Stock_Index', table_col_stock_index, df_stock_index)

def insert_index_price_data():
    table_col = ('Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Index_ID')
    table_name = 'Index_Price'
    datasets = ['datasets/HistoricalData_SPX.csv', 'datasets/HistoricalData_IXIC.csv', 'datasets/HistoricalData_DJIA.csv',
                'datasets/HistoricalData_NDX.csv', 'datasets/HistoricalData_RUT.csv']
    for filename in datasets:
        df, index_symbol = get_dataframe_index(filename)
        index_symbol = index_symbol.split()
        index_symbol.append('')
        row = get_data_from_table('Index_ID', 'Index_Symbol', index_symbol, 'Indexes')
        df['Index_ID'] = row[0][0]
        insert_data(table_name, table_col, df)

def insert_stock_price_data():
    table_col = ('Stock_ID', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume')
    table_name = 'Stock_Price'
    dir = 'datasets/Stocks/'
    datasets = [file for file in os.listdir(os.getcwd()+'\datasets\Stocks')]
    for filename in datasets:
        df, stock_symbol = get_dataframe_stock(dir + filename)
        stock_symbol = stock_symbol.split()
        stock_symbol.append('')
        row = get_data_from_table('Stock_ID', 'Stock_Symbol', stock_symbol, 'Stocks')
        if len(row) > 0:
            df['Stock_ID'] = pd.DataFrame(row*df.size)
            df_stock_price = df[list(table_col)]
            insert_data(table_name, table_col, df_stock_price)

# only call once while creating the db and tables
#initialize_database()
#Inserting Index and Stock data on Initializing
#insert_index_info()
#insert_stock_info()
#Inserting Index data only on Initializing
#insert_index_price_data()
#Insterting Stock Data only on Initializing
#insert_stock_price_data()