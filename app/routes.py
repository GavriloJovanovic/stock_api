# app/routes.py

from flask import Blueprint, request, jsonify
from app.models import db, Stock
from datetime import datetime

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