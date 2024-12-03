import sqlite3
import pandas as pd
from datetime import datetime
import requests
import os
from typing import Dict, Any
import time
import streamlit as st

class StockDatabase:
    def __init__(self, db_name: str = "data/sqlite_db/stock_data.db"):
        self.db_name = db_name
        self.alpha_vantage_api_key = st.secrets['ALPHA_VANTAGE_API']
        self.initialize_database()

    def initialize_database(self):
        """Create the database and required tables if they don't exist"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Create company overview table to store company overview information
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS company_overview (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT PRIMARY KEY,
                asset_type TEXT,
                name TEXT,
                description TEXT,
                cik TEXT,
                exchange TEXT,
                currency TEXT,
                country TEXT,
                sector TEXT,
                industry TEXT,
                address TEXT,
                fiscal_year_end TEXT,
                latest_quarter TEXT,
                market_capitalization INTEGER,
                ebitda INTEGER,
                pe_ratio REAL,
                peg_ratio REAL,
                book_value REAL,
                dividend_per_share REAL,
                dividend_yield REAL,
                eps REAL,
                revenue_per_share_ttm REAL,
                profit_margin REAL,
                operating_margin_ttm REAL,
                return_on_assets_ttm REAL,
                return_on_equity_ttm REAL,
                revenue_ttm INTEGER,
                gross_profit_ttm INTEGER,
                diluted_eps_ttm REAL,
                quarterly_earnings_growth_yoy REAL,
                quarterly_revenue_growth_yoy REAL,
                analyst_target_price REAL,
                trailing_pe REAL,
                forward_pe REAL,
                price_to_sales_ratio_ttm REAL,
                price_to_book_ratio REAL,
                ev_to_revenue REAL,
                ev_to_ebitda REAL,
                beta REAL,
                week_52_high REAL,
                week_52_low REAL,
                day_50_moving_average REAL,
                day_200_moving_average REAL,
                shares_outstanding INTEGER,
                shares_float INTEGER,
                shares_short INTEGER,
                shares_short_prior_month INTEGER,
                short_ratio REAL,
                short_percent_outstanding REAL,
                short_percent_float REAL,
                percent_insiders REAL,
                percent_institutions REAL,
                forward_annual_dividend_rate REAL,
                forward_annual_dividend_yield REAL,
                payout_ratio REAL,
                last_split_factor TEXT,
                last_split_date TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(symbol)
            )
        ''')

        # Create OHLCV table for daily data
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT,
                date DATE,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume INTEGER,
                UNIQUE(symbol, date),
                FOREIGN KEY(symbol) REFERENCES company_overview(symbol)
            )
        ''')

        # Create indexes for faster queries
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_symbol_date 
            ON daily_prices(symbol, date)
        ''')

        conn.commit()
        conn.close()

    def fetch_company_overview(self, symbol: str) -> Dict[str, Any]:
        """Fetch company overview data from Alpha Vantage API"""
        base_url = "https://www.alphavantage.co/query"
        params = {
            "function": "OVERVIEW",
            "symbol": symbol,
            "apikey": self.alpha_vantage_api_key
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching company overview for {symbol}: {e}")
            return None

    def insert_company_overview(self, data: Dict[str, Any]):
        """Insert company overview data into the database"""
        if not data or "Symbol" not in data:
            print("No valid company data received")
            return

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT OR REPLACE INTO company_overview (
                    symbol, asset_type, name, description, cik, exchange, currency, country, sector, industry, address, fiscal_year_end, latest_quarter, market_capitalization, ebitda, pe_ratio, peg_ratio, book_value, dividend_per_share, dividend_yield, eps, revenue_per_share_ttm, profit_margin, operating_margin_ttm, return_on_assets_ttm, return_on_equity_ttm, revenue_ttm, gross_profit_ttm, diluted_eps_ttm, quarterly_earnings_growth_yoy, quarterly_revenue_growth_yoy, analyst_target_price, trailing_pe, forward_pe, price_to_sales_ratio_ttm, price_to_book_ratio, ev_to_revenue, ev_to_ebitda, beta, week_52_high, week_52_low, day_50_moving_average, day_200_moving_average, shares_outstanding, shares_float, shares_short, shares_short_prior_month, short_ratio, short_percent_outstanding, short_percent_float, percent_insiders, percent_institutions, forward_annual_dividend_rate, forward_annual_dividend_yield, payout_ratio, last_split_factor, last_split_date, created_at, updated_at
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                         ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
                ''', (
                data.get('Symbol'),
                data.get('AssetType'),
                data.get('Name'),
                data.get('Description'), 
                data.get('CIK'),
                data.get('Exchange'),
                data.get('Currency'),
                data.get('Country'),
                data.get('Sector'),
                data.get('Industry'),
                data.get('Address'),
                data.get('FiscalYearEnd'),
                data.get('LatestQuarter'),
                self._safe_float(data.get('MarketCapitalization')),
                self._safe_float(data.get('EBITDA')),
                self._safe_float(data.get('PERatio')),
                self._safe_float(data.get('PEGRatio')),
                self._safe_float(data.get('BookValue')),
                self._safe_float(data.get('DividendPerShare')),
                self._safe_float(data.get('DividendYield')),
                self._safe_float(data.get('EPS')),
                self._safe_float(data.get('RevenuePerShareTTM')),
                self._safe_float(data.get('ProfitMargin')),
                self._safe_float(data.get('OperatingMarginTTM')),
                self._safe_float(data.get('ReturnOnAssetsTTM')),
                self._safe_float(data.get('ReturnOnEquityTTM')),
                self._safe_float(data.get('RevenueTTM')),
                self._safe_float(data.get('GrossProfitTTM')),
                self._safe_float(data.get('DilutedEPSTTM')),
                self._safe_float(data.get('QuarterlyEarningsGrowthYOY')),
                self._safe_float(data.get('QuarterlyRevenueGrowthYOY')),
                self._safe_float(data.get('AnalystTargetPrice')),
                self._safe_float(data.get('TrailingPE')),
                self._safe_float(data.get('ForwardPE')),
                self._safe_float(data.get('PriceToSalesRatioTTM')),
                self._safe_float(data.get('PriceToBookRatio')),
                self._safe_float(data.get('EVToRevenue')),
                self._safe_float(data.get('EVToEBITDA')),
                self._safe_float(data.get('Beta')),
                self._safe_float(data.get('52WeekHigh')),
                self._safe_float(data.get('52WeekLow')),
                self._safe_float(data.get('50DayMovingAverage')),
                self._safe_float(data.get('200DayMovingAverage')),
                self._safe_float(data.get('SharesOutstanding')),
                self._safe_float(data.get('SharesFloat')),
                self._safe_float(data.get('SharesShort')),
                self._safe_float(data.get('SharesShortPriorMonth')),
                self._safe_float(data.get('ShortRatio')),
                self._safe_float(data.get('ShortPercentOutstanding')),
                self._safe_float(data.get('ShortPercentFloat')),
                self._safe_float(data.get('PercentInsiders')),
                self._safe_float(data.get('PercentInstitutions')),
                self._safe_float(data.get('ForwardAnnualDividendRate')),
                self._safe_float(data.get('ForwardAnnualDividendYield')),
                self._safe_float(data.get('PayoutRatio')),
                data.get('LastSplitFactor'),
                data.get('LastSplitDate')))
            conn.commit()
            print(f"Successfully inserted company overview for {data.get('Symbol')}")
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            conn.close()

    @staticmethod
    def _safe_float(value):
        """Safely convert value to float, returning None if conversion fails"""
        if value is None:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    def get_company_overview(self, symbol: str) -> Dict[str, Any]:
        """Retrieve company overview from the database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM company_overview WHERE symbol = ?
        ''', (symbol,))
        
        columns = [description[0] for description in cursor.description]
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(zip(columns, row))
        return None

    def fetch_daily_data(self, symbol: str) -> Dict[str, Any]:
        """Fetch daily data from Alpha Vantage API"""
        base_url = "https://www.alphavantage.co/query"
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "apikey": self.alpha_vantage_api_key,
            "outputsize": "compact"
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # Raise exception for bad status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None

    def insert_daily_data(self, symbol: str, data: Dict[str, Any]):
        """Insert daily data into the database"""
        if not data or "Time Series (Daily)" not in data:
            print(f"No valid data received for {symbol}")
            return

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        time_series = data.get("Time Series (Daily)", {})
        
        for date, values in time_series.items():
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO daily_prices 
                    (symbol, date, open, high, low, close, volume)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    symbol,
                    date,
                    float(values['1. open']),
                    float(values['2. high']),
                    float(values['3. low']),
                    float(values['4. close']),
                    int(values['5. volume'])
                ))
            except sqlite3.Error as e:
                print(f"Error inserting data for {symbol} at {date}: {e}")
            except ValueError as e:
                print(f"Value error for {symbol} at {date}: {e}")

        # Update last_updated timestamp in stocks table
        cursor.execute('''
            INSERT OR REPLACE INTO stocks (symbol, last_updated)
            VALUES (?, datetime('now'))
        ''', (symbol,))

        conn.commit()
        conn.close()

    def get_stock_data(self, symbol: str) -> pd.DataFrame:
        """Retrieve stock data from the database"""
        query = '''
            SELECT date, open, high, low, close, volume
            FROM daily_prices 
            WHERE symbol = ?
            ORDER BY date
            LIMIT 5
        '''
        params = [symbol]

        conn = sqlite3.connect(self.db_name)
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()

        # Convert date string to datetime
        df['date'] = pd.to_datetime(df['date'])
        return df

    def get_latest_date(self, symbol: str) -> str:
        """Get the most recent date for a symbol in the database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT MAX(date) FROM daily_prices WHERE symbol = ?
        ''', (symbol,))
        
        result = cursor.fetchone()[0]
        conn.close()
        return result

def main():
    # Initialize the database
    db = StockDatabase()
    
    # Example usage
    symbols = ['AAPL', 'NVDA', 'GOOGL'] 

    for symbol in symbols:
        try:
            print(f"Fetching data for {symbol}...")
            latest_date = db.get_latest_date(symbol)
            
            if latest_date:
                print(f"Latest data for {symbol} is from {latest_date}")
            
            data = db.fetch_daily_data(symbol)
            
            if not data:
                print(f"No data received for {symbol}")
                continue

            if "Error Message" in data:
                print(f"Error fetching data for {symbol}: {data['Error Message']}")
                continue

            db.insert_daily_data(symbol, data)
            print(f"Successfully inserted data for {symbol}")

            # Add delay to respect API rate limits
            time.sleep(12)  # Alpha Vantage has a rate limit of 5 calls per minute for free tier

        except Exception as e:
            print(f"Error processing {symbol}: {str(e)}")

    # Example of retrieving and analyzing data
    aapl_data = db.get_stock_data('AAPL')
    
    if not aapl_data.empty:
        print("\nSample of AAPL data:")
        print(aapl_data.head())

def create_database():
    main()
