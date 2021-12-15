import sqlite3
from sqlite3 import Error
import pandas as pd


# connection = cx_Oracle.connect(
#   user="shikhatomar93",
#  password="12345",
# dsn="localhost:1521/xepdb1")

# print("Successfully connected to Oracle Database")

# cursor = connection.cursor()

# Create a table

# cursor.execute("""
#   begin
#      execute immediate 'drop table todoitem';
#     exception when others then if sqlcode <> -942 then raise; end if;
# end;""")

# cursor.execute("""
#   create table todoitem (
#      id number generated always as identity,
#     description varchar2(4000),
#    creation_ts timestamp with time zone default current_timestamp,
#   done number(1,0),
#  primary key (id))""")

# Insert some data

# rows = [ ("Task 1", 0 ),
#        ("Task 2", 0 ),
#       ("Task 3", 1 ),
#      ("Task 4", 0 ),
#     ("Task 5", 1 ) ]

# cursor.executemany("insert into todoitem (description, done) values(:1, :2)", rows)
# print(cursor.rowcount, "Rows Inserted")

# connection.commit()

# for row in cursor.execute('select description, done from todoitem'):
# Now query the rows back
#   if (row[1]):
# else:
#      print(row[0], "is NOT done")
def create_connection(db_file, delete_db=False):
    import os
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

conn = create_connection("stockMarketDb.db", delete_db=False)
cur = conn.cursor()
def initialDBCreationAndInsertion():
    sql_statement = """
            CREATE TABLE Indexes 
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 DATE TEXT,
                 CLOSE REAL,
                 OPEN REAL,
                 High REAL,
                 LOW REAL,
                 IndexID INTEGER, 
                 FOREIGN KEY(IndexID) REFERENCES DistinctIndexes(IndexID)             
                );"""
    create_table(sql_statement, 'Indexes')
    # table to store distinct indexes and their stocks name
    sql_statement = """
            CREATE TABLE DistinctIndexes 
                (IndexID INTEGER PRIMARY KEY AUTOINCREMENT,
                 Index_Symbol TEXT NOT NULL,
                 Index_Name TEXT NOT NULL 
                );"""
    create_table(sql_statement, 'DistinctIndexes')
    # creating table for the prices of all the stocks
    sql_statement = """
            CREATE TABLE Stocks 
                (StockID INTEGER PRIMARY KEY AUTOINCREMENT,
                 Stock_Symbol TEXT NOT NULL,
                 IndexID INTEGER NOT NULL,
                 FOREIGN KEY(IndexID) REFERENCES DistinctIndexes(IndexID) 
                );"""
    create_table(sql_statement, 'Stocks')
    # creating table for the prices of all the stocks
    sql_statement = """
            CREATE TABLE Prices 
                (PriceID INTEGER PRIMARY KEY AUTOINCREMENT,
                 StockID INTEGER, 
                 DATE REAL,
                 CLOSE REAL,
                 OPEN REAL,
                 High REAL,
                 LOW REAL,
                 FOREIGN KEY(StockID) REFERENCES Stocks(StockID)          
                );"""
    create_table(sql_statement, 'Prices')


# inserting index and stocks data in the table
def insertIndexAndStockData():
    index_data = [('COMP', 'Nasdaq Composite'), ('DJIA', 'Dow Jones Industrial Average'),
                  ('NDX', 'Nasdaq 100'), ('RUT', 'Russell 2000'), ('SPX', 'S&P 500')]
    cur.executemany(f"INSERT INTO DistinctIndexes(Index_Symbol, Index_Name) VALUES(?,?);", index_data)

    stocks_data = []
    cur.executemany(f"INSERT INTO Stocks(Stock_Symbol, IndexID) VALUES(?,?);", stocks_data)
    conn.commit()

# inserting index prices and stocks prices in the table
def insertData(filename, tablename, tableCol):
    df = pd.read_csv(filename)
    df = df.drop('Volume', axis=1)
    df = df.dropna()
    sub = filename.split('_')[1][:-4]
    row = execute_sql_statement(f"select IndexID from DistinctIndexes where Index_Symbol='{sub}'")
    df['IndexID'] = row[0][0]
    cur.executemany(f"INSERT INTO {tablename}{tableCol} VALUES(?,?,?,?,?,?);", df.values.tolist())
    conn.commit()
    del df

def insertIndexPriceData():
    tableCol = ('Date', 'Close', 'Open', 'High', 'Low', 'IndexID')
    insertData('datasets/HistoricalData_SPX.csv', 'Indexes', tableCol)
    insertData('datasets/HistoricalData_COMP.csv', 'Indexes', tableCol)
    insertData('datasets/HistoricalData_DJIA.csv', 'Indexes', tableCol)
    insertData('datasets/HistoricalData_NDX.csv', 'Indexes', tableCol)
    insertData('datasets/HistoricalData_RUT.csv', 'Indexes', tableCol)

def insertStockPriceData():
    tableCol = ('Date', 'Close', 'Open', 'High', 'Low', 'IndexID')
    insertData('datasets/HistoricalData_SPX.csv', 'Prices', tableCol)
    insertData('datasets/HistoricalData_COMP.csv', 'Prices', tableCol)
    insertData('datasets/HistoricalData_DJIA.csv', 'Prices', tableCol)
    insertData('datasets/HistoricalData_NDX.csv', 'Prices', tableCol)
    insertData('datasets/HistoricalData_RUT.csv', 'Prices', tableCol)

# only call once while creating the db and tables
initialDBCreationAndInsertion()
#Inserting Index and Stock data on Initializing
insertIndexAndStockData()
#Inserting Index data only on Initializing
insertIndexPriceData()
#Insterting Stock Data only on Initializing
# insertStockPriceData()