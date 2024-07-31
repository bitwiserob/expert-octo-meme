import yfinance as yf
from datetime import datetime, timedelta
from nicegui import ui
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np


with ui.button('Click me!', on_click=lambda: badge.set_text(int(badge.text) + 1)):
    badge = ui.badge('0', color='red').props('floating')


ui.run()
