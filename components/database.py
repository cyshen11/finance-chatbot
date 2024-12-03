import pandas as pd
from sqlalchemy import create_engine
import yfinance as yf

def create_database():
  # Set up the SQLite database engine
  engine = create_engine('sqlite:///data/sqlite_db.db')

  # Define the stock symbols and date range for data extraction
  symbols = ['AAPL', 'NVDA', 'GOOG']
  start_date = '2024-01-01'
  end_date = '2024-11-30'

  # Extract data from Yahoo Finance
  data = pd.DataFrame()
  for symbol in symbols:
      ticker = yf.Ticker(symbol)
      stock_data = ticker.history(start=start_date, end=end_date)
      stock_data['symbol'] = symbol
      data = pd.concat([data, stock_data])

  # Clean and transform the data
  data = data.reset_index()
  data = data.drop(['Dividends', 'Stock Splits'], axis=1)
  data = data.rename(columns={'Date': 'date', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume', 'symbol': 'symbol'})

  # Load the data into the SQLite database
  data.to_sql('stock_data', engine, index=False, if_exists='replace')

def test_database():
  # Set up the SQLite database engine
  engine = create_engine('sqlite:///data/sqlite_db.db')

  # Query the database
  query = 'SELECT * FROM stock_data LIMIT 10'
  query_result = pd.read_sql(query, engine)

  # Return the query result
  return query_result