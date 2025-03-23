# app/logic.py

import pandas as pd
from app.models import Stock, StockPrice

class StockLogic:

    # Method that loads data by symbol of the company that we want to analyze
    @staticmethod
    def load_stock_data(symbol):
        stock = Stock.query.filter_by(symbol=symbol).first()
        if not stock:
            raise ValueError(f"Symbol '{symbol}' not found.")

        prices = StockPrice.query.filter_by(stock_id=stock.id).order_by(StockPrice.date).all()

        data = [{
            "date": p.date,
            "close": p.close
        } for p in prices]

        return pd.DataFrame(data)

    # Method that get for start_date and end_date the best range for buying/selling for profit
    @staticmethod
    def get_best_trade(df, start_date, end_date):
        df_range = df[(df["date"] >= start_date) & (df["date"] <= end_date)].copy()
        df_range = df_range.reset_index(drop=True)

        max_profit = 0
        buy_date = sell_date = None
        buy_price = sell_price = 0

        for i in range(len(df_range)):
            for j in range(i + 1, len(df_range)):
                buy = df_range.iloc[i]
                sell = df_range.iloc[j]
                profit = sell["close"] - buy["close"]
                if profit > max_profit:
                    max_profit = profit
                    buy_date = buy["date"]
                    sell_date = sell["date"]
                    buy_price = buy["close"]
                    sell_price = sell["close"]

        return {
            "buy_date": buy_date.strftime("%Y-%m-%d") if buy_date else None,
            "buy_price": round(buy_price, 2),
            "sell_date": sell_date.strftime("%Y-%m-%d") if sell_date else None,
            "sell_price": round(sell_price, 2),
            "profit": round(max_profit, 2)
        }

    # Method that calculates the total_profit for company in time period between start and end
    @staticmethod
    def get_total_profit(df, start_date, end_date):
        df_range = df[(df["date"] >= start_date) & (df["date"] <= end_date)].copy()
        df_range = df_range.reset_index(drop=True)

        profit = 0
        for i in range(1, len(df_range)):
            if df_range["close"][i] > df_range["close"][i - 1]:
                profit += df_range["close"][i] - df_range["close"][i - 1]

        return round(profit, 2)