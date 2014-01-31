import app
import ystockquote
import math

def expand_amount_string(amt_str):
    dollar_type = amt_str[-1]
    if dollar_type == 'B':
        return int(float(amt_str[:-1]) * math.pow(10,9))
    elif dollar_type == 'M':
        return int(float(amt_str[:-1]) * math.pow(10,6))
    else:
        print 'Unknown dollar_type'
        return None

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

@app.sched.cron_schedule(day_of_week='mon-fri', hour='15,18,21')
def update_records():
    time = app.utility.get_time()
    count = 0
    fail = 0
    for equity in app.models.equities_from_exchange('NYSE'):
        try:
            print 'Working Equity %s' % equity.ticker
            data = ystockquote.get_all(equity.ticker)
            if data['price'] == 'N/A':
                print 'Price is NA. Killing'
                continue

            data = cleanse_data(data)
            record = app.models.create_record(
                time, data['volume'], data['stock_exchange'],
                data['price'], data['market_cap'], data['short_ratio'],
                data['price_sales_ratio'], data['price_earnings_ratio'],
                data['earnings_per_share'], data['fifty_day_moving_avg'],
                data['two_hundred_day_moving_avg'])
            count += 1
            app.utility.commit()
        except Exception, e:
            print 'FAIL: %s, %s' % (equity.ticker, data)
            fail += 1
    print 'Completed: %d, Failed: %d' % (count, fail)

