import app
from flask import render_template, request, jsonify
# from flask.ext.login import logout_user, login_required, login_user

@app.flask_app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

def equity_halves(equities):
    first_half = equities[0:(len(equities)/2)]
    second_half = None
    if len(first_half) < len(equities):
        second_half = equities[len(first_half):(len(equities)-1)]
    return first_half, second_half

@app.flask_app.route('/nyse', methods=['GET'])
def nyse():
    equities = app.models.equities_from_exchange('nyse')
    first_half, second_half = equity_halves(equities)
    return render_template('exchange.html', exchange="NYSE",
                           first_half=first_half, second_half=second_half)

@app.flask_app.route('/nasdaq', methods=['GET'])
def nasdaq():
    equities = app.models.equities_from_exchange('nasdaq')
    first_half, second_half = equity_halves(equities)
    return render_template('exchange.html', exchange="NASDAQ",
                           first_half=first_half, second_half=second_half)

