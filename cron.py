import app
from apscheduler.scheduler import Scheduler
import ystockquote
import math

sched = Scheduler()

dollar_types = {'B':9, 'M':6, 'T':12, 'K':3}
def expand_amount_string(amt_str):
    dollar = amt_str[-1]
    if dollar not in dollar_types:
        print 'Unknown dollar_type %s' % amt_str
        return None
    else:
        return int(float(amt_str[:-1]) * math.pow(10, dollar_types[dollar]))

def cleanse_data(data):
    ret = {}
    for key, value in data.iteritems():
        if value == 'N/A':
            ret[key] = None
        elif key in ['price', 'short_ratio', 'price_sales_ratio', 'price_earnings_ratio',
                     'earnings_per_share', 'fifty_day_moving_avg', 'two_hundred_day_moving_avg']:
            ret[key] = float(value)
        elif key == 'volume':
            ret[key] = int(value)
        elif key == 'stock_exchange':
            ret[key] = value.strip('"')
        elif key == 'market_cap':
            ret[key] = expand_amount_string(value)
    return ret

def _update_record(equity, time):
    data = ystockquote.get_all(equity.ticker)
    if data['price'] == 'N/A':
        print 'Price is NA. Killing'
        return None

    data = cleanse_data(data)
    record = app.models.create_record(
        time, data['volume'], data['stock_exchange'],
        data['price'], data['market_cap'], data['short_ratio'],
        data['price_sales_ratio'], data['price_earnings_ratio'],
        data['earnings_per_share'], data['fifty_day_moving_avg'],
        data['two_hundred_day_moving_avg'], equity.id)
    return data

def _update_records(exchange, time):
    print 'Starting Exchange %s' % exchange
    count = 0
    fail = 0
    for equity in app.models.equities_from_exchange(exchange):
        try:
            data = _update_record(equity, time)
            if not data:
                continue
            count += 1
        except Exception, e:
            print 'FAIL: %s, %s' % (equity.ticker, data)
            print e
            fail += 1
        finally:
            app.utility.commit()
    print 'Completed: %d, Failed: %d' % (count, fail)

@sched.cron_schedule(day_of_week='mon-fri', hour='15,18,21')
def update_records():
    time = app.utility.get_time()
    print 'Starting update at time %s' % time
    _update_records('NYSE', time)
    _update_records('NASDAQ', time)
    print 'Finished updating at time %s' % app.utility.get_time()

# sched.start()

