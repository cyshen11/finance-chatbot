import sqlite3
import yfinance as yf
from datetime import datetime
import pandas as pd

def create_tables():
    conn = sqlite3.connect('data/sqlite_db.db')
    cursor = conn.cursor()

    # Create Companies table to store basic ticker information
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS companies (
        ticker_id TEXT PRIMARY KEY,
        company_name TEXT,
        sector TEXT,
        industry TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create Historical Price Data table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS price_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker_id TEXT,
        date DATE,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume INTEGER,
        dividends REAL,
        stock_splits REAL,
        FOREIGN KEY (ticker_id) REFERENCES companies(ticker_id),
        UNIQUE(ticker_id, date)
    )
    ''')

    # Create Balance Sheet table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS balance_sheets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker_id TEXT,
        date DATE,
        inventory REAL,
        FOREIGN KEY (ticker_id) REFERENCES companies(ticker_id),
        UNIQUE(ticker_id, date)
    )
    ''')

    # Create Income Statement table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS income_statements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker_id TEXT,
        date DATE,
        ebit REAL,
        ebitda REAL,
        FOREIGN KEY (ticker_id) REFERENCES companies(ticker_id),
        UNIQUE(ticker_id, date)
    )
    ''')

    conn.commit()
    conn.close()

def insert_ticker_data(symbol):
    conn = sqlite3.connect('data/sqlite_db.db')
    cursor = conn.cursor()
    
    ticker = yf.Ticker(symbol)
    
    # Insert company info
    try:
        info = ticker.info
        cursor.execute('''
        INSERT OR REPLACE INTO companies (ticker_id, company_name, sector, industry)
        VALUES (?, ?, ?, ?)
        ''', (symbol, info.get('longName'), info.get('sector'), info.get('industry')))
    except Exception as e:
        print(f"Error inserting company info: {e}")

    # Insert historical data
    try:
        history = ticker.history(period="max")
        for date, row in history.iterrows():
            cursor.execute('''
            INSERT OR REPLACE INTO price_history 
            (ticker_id, date, open, high, low, close, volume, dividends, stock_splits)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                symbol,
                date.strftime('%Y-%m-%d'),
                row['Open'],
                row['High'],
                row['Low'],
                row['Close'],
                row['Volume'],
                row['Dividends'],
                row['Stock Splits']
            ))
    except Exception as e:
        print(f"Error inserting price history: {e}")

    # Insert balance sheet data
    try:
        balance_sheet = ticker.get_balance_sheet()
        for date, data in balance_sheet.items():
            cursor.execute('''
            INSERT OR REPLACE INTO balance_sheets 
            (ticker_id, date, inventory)
            VALUES (?, ?, ?)
            ''', (
                symbol,
                date.strftime('%Y-%m-%d'),
                data.get('Inventory')
            ))
    except Exception as e:
        print(f"Error inserting balance sheet data: {e}")

    # Insert income statement data
    try:
        income_stmt = ticker.get_income_stmt()
        for date, data in income_stmt.items():
            cursor.execute('''
            INSERT OR REPLACE INTO income_statements 
            (ticker_id, date, ebit, ebitda)
            VALUES (?, ?, ?, ?)
            ''', (
                symbol,
                date.strftime('%Y-%m-%d'),
                data.get('EBIT'),
                data.get('EBITDA')
            ))
    except Exception as e:
        print(f"Error inserting income statement data: {e}")

    conn.commit()
    conn.close()

# Usage example
def create_database():
    create_tables()
    insert_ticker_data("AAPL")
    insert_ticker_data("NVDA")
    insert_ticker_data("GOOG")

def test_database():
    conn = sqlite3.connect('file:data/sqlite_db.db?mode=ro', uri=True)
    df_companies = pd.read_sql_query("SELECT * FROM companies LIMIT 5", conn)
    df_price_history = pd.read_sql_query("SELECT * FROM price_history LIMIT 5", conn)
    df_balance_sheets = pd.read_sql_query("SELECT * FROM balance_sheets LIMIT 5", conn)
    df_income_statements = pd.read_sql_query("SELECT * FROM income_statements LIMIT 5", conn)
    conn.close()
    return df_companies, df_price_history, df_balance_sheets, df_income_statements

