import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
import os
import requests
import mysql.connector



class alphaStrats(self):
    def btcDCA(self):
        endDate = dt.datetime.today().strftime("%Y-%m-%d")
        startDate = #last date in database
        btc = yf.Ticker("BTC-USD")
        btcWeekly = btc.download(period="max",end=endDate, start=startDate, interval="1wk")
        
