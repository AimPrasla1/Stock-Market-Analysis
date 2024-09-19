from flask import Flask, render_template, request, jsonify
import yfinance as yf
import pandas as pd

app = Flask(__name__)

def fetch_stock_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    stock1 = request.form.get('stock1')
    stock2 = request.form.get('stock2')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    stock1_data = fetch_stock_data(stock1, start_date, end_date)
    stock2_data = fetch_stock_data(stock2, start_date, end_date)

    stock1_json = stock1_data[['Adj Close']].reset_index().to_dict(orient='records')
    stock2_json = stock2_data[['Adj Close']].reset_index().to_dict(orient='records')

    return jsonify({
        'stock1': stock1_json,
        'stock2': stock2_json
    })

if __name__ == '__main__':
    app.run(debug=True)
