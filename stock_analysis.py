import pandas as pd
import yfinance as yf
import plotly.io as pio
import plotly.graph_objects as go


# Set default template for plotly visuals
pio.templates.default = "plotly_white"

# Function to fetch stock data
def fetch_stock_data(ticker, start_date, end_date):
    return yf.download(ticker, start=start_date, end=end_date)

# Step 1: Take user input for stock symbols and date range
def get_user_input():
    stock1 = input("Enter the ticker symbol for the first stock (e.g., AAPL): ").upper()
    stock2 = input("Enter the ticker symbol for the second stock (e.g., GOOGL): ").upper()
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    return stock1, stock2, start_date, end_date

# Get user input
stock1_ticker, stock2_ticker, start_date, end_date = get_user_input()

# Step 2: Fetch historical stock price data for the two stocks
stock1_data = fetch_stock_data(stock1_ticker, start_date, end_date)
stock2_data = fetch_stock_data(stock2_ticker, start_date, end_date)

# Step 3: Calculate daily returns for both stocks
stock1_data['Daily_Return'] = stock1_data['Adj Close'].pct_change()
stock2_data['Daily_Return'] = stock2_data['Adj Close'].pct_change()

# Step 4: Visualize daily returns
def plot_daily_returns(stock1_data, stock2_data, stock1_ticker, stock2_ticker):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stock1_data.index, y=stock1_data['Daily_Return'],
                             mode='lines', name=stock1_ticker, line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=stock2_data.index, y=stock2_data['Daily_Return'],
                             mode='lines', name=stock2_ticker, line=dict(color='green')))
    fig.update_layout(title=f'Daily Returns for {stock1_ticker} and {stock2_ticker} (Selected Period)',
                      xaxis_title='Date', yaxis_title='Daily Return',
                      legend=dict(x=0.02, y=0.95))
    fig.show()

# Plot daily returns
plot_daily_returns(stock1_data, stock2_data, stock1_ticker, stock2_ticker)

# Step 5: Calculate cumulative returns for both stocks
stock1_cumulative_return = (1 + stock1_data['Daily_Return']).cumprod() - 1
stock2_cumulative_return = (1 + stock2_data['Daily_Return']).cumprod() - 1

# Step 6: Visualize cumulative returns
def plot_cumulative_returns(stock1_cumulative_return, stock2_cumulative_return, stock1_ticker, stock2_ticker):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stock1_cumulative_return.index, y=stock1_cumulative_return,
                             mode='lines', name=stock1_ticker, line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=stock2_cumulative_return.index, y=stock2_cumulative_return,
                             mode='lines', name=stock2_ticker, line=dict(color='green')))
    fig.update_layout(title=f'Cumulative Returns for {stock1_ticker} and {stock2_ticker} (Selected Period)',
                      xaxis_title='Date', yaxis_title='Cumulative Return',
                      legend=dict(x=0.02, y=0.95))
    fig.show()

# Plot cumulative returns
plot_cumulative_returns(stock1_cumulative_return, stock2_cumulative_return, stock1_ticker, stock2_ticker)

# Step 7: Calculate and compare volatility (standard deviation of daily returns)
stock1_volatility = stock1_data['Daily_Return'].std()
stock2_volatility = stock2_data['Daily_Return'].std()

def plot_volatility_comparison(stock1_volatility, stock2_volatility, stock1_ticker, stock2_ticker):
    fig = go.Figure()
    fig.add_bar(x=[stock1_ticker, stock2_ticker], y=[stock1_volatility, stock2_volatility],
                text=[f'{stock1_volatility:.4f}', f'{stock2_volatility:.4f}'],
                textposition='auto', marker=dict(color=['blue', 'green']))
    fig.update_layout(title=f'Volatility Comparison ({stock1_ticker} vs {stock2_ticker})',
                      xaxis_title='Stock', yaxis_title='Volatility (Standard Deviation)',
                      bargap=0.5)
    fig.show()

# Plot volatility comparison
plot_volatility_comparison(stock1_volatility, stock2_volatility, stock1_ticker, stock2_ticker)

# Step 8: Compare stocks against the market benchmark (S&P 500)
market_data = fetch_stock_data('^GSPC', start_date, end_date)  # S&P 500 as benchmark

# Calculate daily returns for the market benchmark
market_data['Daily_Return'] = market_data['Adj Close'].pct_change()

# Step 9: Calculate Beta (sensitivity to market movements)
def calculate_beta(stock_data, market_data):
    covariance = stock_data['Daily_Return'].cov(market_data['Daily_Return'])
    variance = market_data['Daily_Return'].var()
    beta = covariance / variance
    return beta

beta_stock1 = calculate_beta(stock1_data, market_data)
beta_stock2 = calculate_beta(stock2_data, market_data)

# Step 10: Compare Beta values
def compare_beta(beta_stock1, beta_stock2, stock1_ticker, stock2_ticker):
    if beta_stock1 > beta_stock2:
        conclusion = f"{stock1_ticker} is more volatile (higher Beta) compared to {stock2_ticker}."
    else:
        conclusion = f"{stock2_ticker} is more volatile (higher Beta) compared to {stock1_ticker}."
    print(f'Beta for {stock1_ticker}: {beta_stock1:.4f}\nBeta for {stock2_ticker}: {beta_stock2:.4f}\n{conclusion}')

# Compare beta values
compare_beta(beta_stock1, beta_stock2, stock1_ticker, stock2_ticker)
