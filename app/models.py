from . import db

class Stock(db.Model):
    __tablename__ = 'stocks'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    symbol = db.Column(db.String(10), nullable=False, unique=True)
    founded = db.Column(db.Date, nullable=False)

    prices = db.relationship('StockPrice', backref='stock', cascade="all, delete-orphan")


class StockPrice(db.Model):
    __tablename__ = 'stock_prices'

    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    open = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    close = db.Column(db.Float, nullable=False)
    adj_close = db.Column(db.Float)
    volume = db.Column(db.BigInteger)