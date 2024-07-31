import yfinance as yf
from datetime import datetime, timedelta
from nicegui import ui
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# Fetching daily stock data for a given ticker (e.g., AAPL)
def fetch_stock_data(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    end_date = datetime.today()
    start_date = end_date - timedelta(days=30)  # Fetch data for the last 30 days
    hist = ticker.history(start=start_date, end=end_date, interval="1d")
    hist.reset_index(inplace=True)
    
    # Convert Timestamp to string for JSON serialization
    hist['Date'] = hist['Date'].dt.strftime('%Y-%m-%d')
    
    return hist

# Prepare the data for the grid
stock_data = fetch_stock_data("AAPL")
row_data = stock_data.to_dict(orient="records")

grid = ui.aggrid({
    'defaultColDef': {'flex': 1},
    'columnDefs': [
        {'headerName': 'Date', 'field': 'Date', 'sortable': True, 'filter': True},
        {'headerName': 'Open', 'field': 'Open', 'sortable': True, 'filter': True},
        {'headerName': 'High', 'field': 'High', 'sortable': True, 'filter': True},
        {'headerName': 'Low', 'field': 'Low', 'sortable': True, 'filter': True},
        {'headerName': 'Close', 'field': 'Close', 'sortable': True, 'filter': True},
        {'headerName': 'Volume', 'field': 'Volume', 'sortable': True, 'filter': True},
        {'headerName': 'Predicted Close', 'field': 'Predicted Close', 'sortable': True, 'filter': True},
    ],
    'rowData': row_data,
    'rowSelection': 'multiple',
}).classes('max-h-40')

# Function to update the grid with new data and predictions
def update_grid():
    new_data = fetch_stock_data("AAPL")
    
    # Training a regression model
    new_data['Date'] = pd.to_datetime(new_data['Date'])
    new_data['Day'] = (new_data['Date'] - new_data['Date'].min()).dt.days
    X = new_data[['Day']]
    y = new_data['Close']
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Making predictions
    new_data['Predicted Close'] = model.predict(X)
    
    # Convert Date back to string for JSON serialization
    new_data['Date'] = new_data['Date'].dt.strftime('%Y-%m-%d')
    
    # Update grid data
    grid.options['rowData'] = new_data.to_dict(orient="records")
    grid.update()


with ui.button('Click me!', on_click=lambda: badge.set_text(int(badge.text) + 1)):
    badge = ui.badge('0', color='red').props('floating')



ui.button('Update Data', on_click=update_grid)
ui.button('Select All', on_click=lambda: grid.run_grid_method('selectAll'))

ui.run()
