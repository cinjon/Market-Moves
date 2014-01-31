import app
from app import db

class Equity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), index=True)
    name = db.Column(db.String(100))
    exchange = db.Column(db.String(30), index=True)
    sector = db.Column(db.String(100), index=True)
    industry = db.Column(db.String(150), index=True)

    def __init__(self, ticker, name, exchange, sector, industry):
        self.ticker = ticker
        self.name = name
        self.exchange = exchange
        self.sector = sector
        self.industry = industry

def equities_from_exchange(exchange):
    return Equity.query.filter_by(exchange=exchange).all()

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    volume = db.Column(db.Integer)
    exchange = db.Column(db.String(30))
    price = db.Column(db.Float)
    market_cap = db.Column(db.Integer)
    short_ratio = db.Column(db.Float)
    ps = db.Column(db.Float)
    pe = db.Column(db.Float)
    eps = db.Column(db.Float)
    fifty_day_avg = db.Column(db.Float)
    twohund_day_avg = db.Column(db.Float)

    def __init__(self, timestamp, volume, exchange, price, market_cap,
                 short_ratio, ps, pe, eps, fifty_day_avg, twohund_day_avg):
        self.timestamp = timestamp or app.utility.get_time()
        self.volume = volume
        self.exchange = exchange
        self.price = price
        self.market_cap = market_cap
        self.short_ratio = short_ratio
        self.ps = ps
        self.pe = pe
        self.eps = eps
        self.fifty_day_avg = fifty_day_avg
        self.twohund_day_avg = twohund_day_avg
