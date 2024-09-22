from flask import Flask, render_template, request, jsonify
import yfinance as yf
import pandas as pd

app = Flask(__name__)

# Function to fetch stock data using yfinance
def fetch_stock_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

# Route to render the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle stock data analysis
@app.route('/analyze', methods=['POST'])
def analyze():
    stock1 = request.form.get('stock1')
    stock2 = request.form.get('stock2')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    # Fetch data for both stocks using the correct field names for OHLC
    stock1_data = fetch_stock_data(stock1, start_date, end_date)
    stock2_data = fetch_stock_data(stock2, start_date, end_date)

    # Prepare the response data for both stocks (ensure Close field is used)
    stock1_json = stock1_data[['Open', 'High', 'Low', 'Close', 'Volume']].reset_index().to_dict(orient='records')
    stock2_json = stock2_data[['Open', 'High', 'Low', 'Close', 'Volume']].reset_index().to_dict(orient='records')

    return jsonify({
        'stock1': stock1_json,
        'stock2': stock2_json
    })

if __name__ == '__main__':
    app.run(debug=True)
