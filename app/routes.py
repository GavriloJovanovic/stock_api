from flask import Blueprint

stock_bp = Blueprint('stock', __name__)

@stock_bp.route("/")
def index():
    return "API works!"