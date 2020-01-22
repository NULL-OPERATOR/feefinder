import json

from flask import render_template, jsonify, request

from app import app
from utils import calculator


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/calculate_fee', methods=['GET'])
def calculate_fee():
    """
    takes a term/amount as query parameters
    returns term/amount/fee
    """
    term = request.values.get("term", type=int, default=12)
    amount = request.values.get("amount", type=int, default=10000)

    # just basic input validation
    if term not in [12, 24]:
        term = 12

    if amount > 20000:
        amount = 20000
    elif amount < 1000:
        amount = 1000

    fee = calculator(term, amount)

    return jsonify({
        'amount': amount,
        'fee': fee,
        'term': term
    })
