import string
import yfinance as yf
import datetime as dt
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.io as pio
from requests.exceptions import HTTPError

# Set the date range
end = dt.datetime.now()
start = end - dt.timedelta(days=5*365)  # 5 years ago

#FUNCTIONS------------------------------------------------------------------

#To check if given stock names exist and return error if not
def is_valid_stock(stock_symbol):
    try:
        # Attempt to create a Ticker object for the input stock symbol
        stock = yf.Ticker(stock_symbol)
        # Try to fetch information about the stock
        stock_info = stock.info
        # If the info is fetched successfully, the stock symbol is valid
        return True
    except HTTPError as e:
        if e.response.status_code == 404:
            # Handle the 404 error (stock not found)
            print(f"Error: Stock symbol '{stock_symbol}' not found.")
            return False
        else:
            # Handle other HTTP errors if needed
            print(f"HTTP Error {e.response.status_code}: An error occurred.")
            return False
        
#MAIN----------------------------------------------------------------------
print("WELCOME TO COMAPRESHARES")
print("Please enter the first stock name")
stock_a = input()
is_valid_stock(stock_a)
print("Please enter the second stock name")
stock_b = input()
is_valid_stock(stock_b)

ticker_a = yf.Ticker(stock_a)
ticker_b = yf.Ticker(stock_b)

# Get the financial data for both stocks
pe_ratio_1 = ticker_a.info["trailingPE"]
eps_1 = ticker_a.info["trailingEps"]
pb_ratio_1 = ticker_a.info["trailingPE"]
dividend_yield_1 = ticker_a.info["dividendYield"] * 100  # Convert to percentage

pe_ratio_2 = ticker_b.info["trailingPE"]
eps_2 = ticker_b.info["trailingEps"]
pb_ratio_2 = ticker_b.info["trailingPE"]
dividend_yield_2 = ticker_b.info["dividendYield"] * 100  # Convert to percentage

# Data for plotting
metrics = ["P/E Ratio", "Earnings Per Share (EPS)","P/B Ratio", "Dividend Yield (%)"]
values_1 = [pe_ratio_1, eps_1,pb_ratio_1, dividend_yield_1]
values_2 = [pe_ratio_2, eps_2,pb_ratio_2, dividend_yield_2]

# Create an array of indices for the metrics
indices = np.arange(len(metrics))

# Set the width of the bars
bar_width = 0.35

# Create grouped bar graphs for the two stocks
plt.figure(figsize=(12, 6))
plt.bar(indices - bar_width/2, values_1, bar_width, label=stock_a, color='blue')
plt.bar(indices + bar_width/2, values_2, bar_width, label=stock_b, color='green')
plt.title("Financial Metrics Comparison")
plt.ylabel("Value")
plt.ylim(min(min(values_1), min(values_2)) - 5, max(max(values_1), max(values_2)) + 5)
plt.xticks(indices, metrics, rotation=15)
plt.legend()

# Add labels to the bars
for i, v1, v2 in zip(indices, values_1, values_2):
    plt.text(i - bar_width/2, v1, f"{v1:.2f}", ha='center', va='bottom', color='black', fontweight='bold')
    plt.text(i + bar_width/2, v2, f"{v2:.2f}", ha='center', va='bottom', color='black', fontweight='bold')

    plt.tight_layout()

# Show the bar graph plots
plt.show()

# Retrieve stock data for plot
stock_data = yf.download(stock_a+" "+stock_b, start=start, end=end, group_by='ticker')
fig = px.line(stock_data.xs('Close', level=1, axis=1), title='Closing Prices (5 years)')

# Show the closing prices last 5 yr line graph
fig.show()
