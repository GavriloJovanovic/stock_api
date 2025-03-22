"""
Script for loading stock price data from CSV files into the SQLite database.
Each row represents the stock price for a given company on a specific date.
"""

import os
import pandas as pd
from datetime import datetime

from app import create_app, db
from app.models import Stock, StockPrice

# Initialize the Flask application context
app = create_app()
app.app_context().push()

DATA_FOLDER = "data"

# Map CSV filenames to stock symbols
file_symbol_map = {
    "Apple.csv": "AAPL",
    "Amazon.csv": "AMZN",
    "Google.csv": "GOOGL",
    "Facebook.csv": "FB",
    "Netflix.csv": "NFLX"
}

# Set founding dates for companies
founded_dates = {
    "AAPL": "1980-12-12",
    "AMZN": "1997-05-15",
    "GOOGL": "2004-08-19",
    "FB": "2012-05-18",
    "NFLX": "2002-05-23"
}

# Load each CSV into the database
for filename in os.listdir(DATA_FOLDER):
    if filename.endswith(".csv"):
        filepath = os.path.join(DATA_FOLDER, filename)
        df = pd.read_csv(filepath)

        symbol = file_symbol_map.get(filename)
        company_name = filename.replace(".csv", "")
        founded_str = founded_dates.get(symbol)

        if not symbol or not founded_str:
            print(f"Skipping {filename}: no mapping found.")
            continue

        # Create Stock entry if not exists
        existing = Stock.query.filter_by(symbol=symbol).first()
        if not existing:
            stock = Stock(
                company_name=company_name,
                symbol=symbol,
                founded=datetime.strptime(founded_str, "%Y-%m-%d").date()
            )
            db.session.add(stock)
            db.session.commit()
        else:
            stock = existing

        # Insert all price records from the CSV
        for _, row in df.iterrows():
            try:
                price = StockPrice(
                    stock_id=stock.id,
                    date=datetime.strptime(row["Date"], "%Y-%m-%d").date(),
                    open=float(row["Open"]),
                    high=float(row["High"]),
                    low=float(row["Low"]),
                    close=float(row["Close"]),
                    adj_close=float(row["Adj Close"]),
                    volume=int(row["Volume"])
                )
                db.session.add(price)
            except Exception as e:
                print(f"Skipping row on {row.get('Date')}: {e}")
                continue

        db.session.commit()
        print(f"Loaded file: {filename}")

