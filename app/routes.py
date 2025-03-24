# app/routes.py

from flask import Blueprint, request, jsonify
from app.models import db, Stock
from datetime import datetime, timedelta

stock_bp = Blueprint('stock', __name__)

def stock_to_dict(stock):
    return {
        "id": stock.id,
        "name": stock.company_name,
        "symbol": stock.symbol,
        "founded": stock.founded.strftime("%Y-%m-%d")
    }

# POST /stocks
@stock_bp.route("/stocks", methods=["POST"])
def create_stock():
    data = request.get_json()
    name = data.get("name")
    symbol = data.get("symbol")
    founded = data.get("founded")

    if not all([name, symbol, founded]):
        return jsonify({"error": "Missing data"}), 400

    # Proveri da li postoji u bazi
    if Stock.query.filter_by(symbol=symbol).first():
        return jsonify({"error": "Stock already exists"}), 409

    stock = Stock(
        company_name=name,
        symbol=symbol,
        founded=datetime.strptime(founded, "%Y-%m-%d").date()
    )

    db.session.add(stock)
    db.session.commit()

    return jsonify(stock_to_dict(stock)), 201

# Read All Stocks
@stock_bp.route("/stocks", methods=["GET"])
def get_all_stocks():
    stocks = Stock.query.all()
    return jsonify([stock_to_dict(s) for s in stocks])

# Read One Stock With Exact Symbol
@stock_bp.route("/stocks/<symbol>", methods=["GET"])
def get_stock(symbol):
    stock = Stock.query.filter_by(symbol=symbol).first()
    if not stock:
        return jsonify({"error": "Stock not found"}), 404
    return jsonify(stock_to_dict(stock))

# Update One Stock By It's Symbol
@stock_bp.route("/stocks/<symbol>", methods=["PUT"])
def update_stock(symbol):
    stock = Stock.query.filter_by(symbol=symbol).first()
    if not stock:
        return jsonify({"error": "Stock not found"}), 404

    data = request.get_json()
    stock.company_name = data.get("name", stock.company_name)
    if data.get("founded"):
        stock.founded = datetime.strptime(data["founded"], "%Y-%m-%d").date()

    db.session.commit()
    return jsonify(stock_to_dict(stock))

# Delete One Stock By It's Symbol
@stock_bp.route("/stocks/<symbol>", methods=["DELETE"])
def delete_stock(symbol):
    stock = Stock.query.filter_by(symbol=symbol).first()
    if not stock:
        return jsonify({"error": "Stock not found"}), 404

    db.session.delete(stock)
    db.session.commit()
    return jsonify({"message": f"Stock {symbol} deleted"})

from .logic import StockLogic

# For company symbol, start_date and end_date we get three peirods for best_profit and total_profit
@stock_bp.route("/stocks/profit", methods=["POST"])
def calculate_profit():
    data = request.get_json()
    symbol = data.get("symbol")
    start = data.get("start_date")
    end = data.get("end_date")

    if not all([symbol, start, end]):
        return jsonify({"error": "Missing data"}), 400

    try:
        df = StockLogic.load_stock_data(symbol)
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()
        delta = end_date - start_date

        # Getting three periods for calculating profits
        before_start = start_date - delta - timedelta(days=1)
        before_end = start_date - timedelta(days=1)

        after_start = end_date + timedelta(days=1)
        after_end = end_date + delta + timedelta(days=1)

        result = {
            "previous": {
                "best_trade": StockLogic.get_best_trade(df, before_start, before_end),
                "total_profit": StockLogic.get_total_profit(df, before_start, before_end)
            },
            "selected": {
                "best_trade": StockLogic.get_best_trade(df, start_date, end_date),
                "total_profit": StockLogic.get_total_profit(df, start_date, end_date)
            },
            "next": {
                "best_trade": StockLogic.get_best_trade(df, after_start, after_end),
                "total_profit": StockLogic.get_total_profit(df, after_start, after_end)
            }
        }

        # Logic that adds another company that can be more profitable

        # Get user's selected profit
        user_profit = result["selected"]["total_profit"]
        more_profitable = []

        # Fetch all stocks from the database
        all_stocks = Stock.query.all()

        for s in all_stocks:
            if s.symbol == symbol:
                continue  # Skip the one already being analyzed

            try:
                # Use the existing static method from StockLogic
                df_alt = StockLogic.load_stock_data(s.symbol)
                alt_profit = StockLogic.get_total_profit(df_alt, start_date, end_date)

                if alt_profit > user_profit:
                    more_profitable.append(s.symbol)
            except Exception as e:
                continue  # Skip stock if there's an error loading data

        # Add the optional info to the response
        result["more_profitable_stocks"] = more_profitable




        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
