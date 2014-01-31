import app
import datetime

start_date = datetime.datetime(year=1970,month=1,day=1)

def get_time():
    return datetime.datetime.utcnow()

def get_unixtime(_datetime=None):
    if _datetime:
        return (_datetime - start_date).total_seconds()
    return (datetime.datetime.utcnow() - start_date).total_seconds()

def add(transaction):
    app.db.session.add(transaction)

def delete(transaction):
    app.db.session.delete(transaction)

def commit():
    app.db.session.commit()

def drop_all():
    app.db.drop_all()
