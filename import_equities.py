import config
import app

d = config.basedir
nasdaq_loc = d + '/nasdaqlist.csv'
nyse_loc = d + '/nyselist.csv'

def import_equity(line):
    split = [d for d in line.split('"') if d != ','][1:]
    return {'ticker':split[0], 'name':split[1], 'sector':split[6], 'industry':split[7]}

def import_equities(f, exchange):
    f = open(f, 'r')
    lines = f.readlines()
    count = 0
    fail = 0
    print 'Starting %s' % exchange
    for line in lines[1:]:
        try:
            data = import_equity(line)
            app.models.create_equity(data['ticker'], data['name'], exchange,
                                     data['sector'], data['industry'])
            count += 1
        except Exception, e:
            fail += 1
    try:
        app.utility.commit()
    except Exception, e:
        print 'Failed to commit'
    print 'Completed: %d' % count
    print 'Failed: %d' % fail

if __name__ == '__main__':
    import_equities(nasdaq_loc, 'NASDAQ')
    import_equities(nyse_loc, 'NYSE')
