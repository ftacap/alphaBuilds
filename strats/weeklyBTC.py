import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
import os
from pathlib import Path

class WeeklyBTC():
    def __init__(self):
        base_dir = Path(__file__).resolve().parents[1]   # alphaBuilds/
        data_dir = base_dir / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        self.path = str(data_dir / "weeklyBTC.csv")
        self.today = dt.datetime.today()
        self.symbol = "BTC-USD"

    def fileExists(self):
        return os.path.exists(self.path)    
  
    
    def get_return(self):
        # if file missing, create it
        if not self.fileExists():
            self.createFile()
        # read file
        df = pd.read_csv(self.path)
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date")
        
        # parse last date properly
        lastDate = pd.to_datetime(df.iloc[-1]["Date"])

        latest_df = yf.download(tickers=self.symbol, period = "2mo", interval = "1wk", progress=False, auto_adjust=False).reset_index()

        if latest_df.empty:
            # fallback: just use local data
            return float(df["Return"].iloc[-1])

        latest_provider_date = pd.to_datetime(latest_df["Date"]).max()
      
        if lastDate < latest_provider_date:
            print("BTC data is out of date, updating...")
            self.update_btc_data()
            df = pd.read_csv(self.path)
            df["Date"] = pd.to_datetime(df["Date"])
            df = df.sort_values("Date")
        
        return float(df.iloc[-1]["Return"])

    
    def createFile(self):
        self.maxBTC()
        return True

    def maxBTC(self):
        fileName = self.path
        btcMaxDownload = yf.download(tickers=self.symbol, period="max", interval="1wk", progress=False, auto_adjust=False)
        btcMaxDownload = btcMaxDownload.reset_index()
        btcMaxDownload = btcMaxDownload[['Date', 'Close']]
        btcMaxDownload['Return'] = np.log(btcMaxDownload['Close']/btcMaxDownload['Close'].shift(1)) * 100
        btcMaxDownload.to_csv(fileName, index=False)
        print(f'BTC Max Downloaded and Saved at {fileName}')
    
    def update_btc_data0(self):
        fileName = self.path
        ticker = self.symbol
        startDate = pd.read_csv(fileName).iloc[-1]['Date']
        endDate = self.today
        btcUpdate = yf.download(tickers=ticker, interval="1wk", start=startDate, end=endDate, progress=False, auto_adjust=False)
        btcUpdate = btcUpdate.reset_index()
        btcUpdate = btcUpdate[['Date', 'Close']]
        btcUpdate['Return'] = np.log(btcUpdate['Close']/btcUpdate['Close'].shift(1)) * 100
        btcUpdate.to_csv(fileName, index=False)
        print(f'BTC Updated and Saved at {fileName}')

    def update_btc_data(self):
        # 1) load existing file
        old = pd.read_csv(self.path)
        old["Date"] = pd.to_datetime(old["Date"])
        old = old.sort_values("Date")

        lastDate = old["Date"].iloc[-1]

        # 2) download with a small overlap window (prevents missing/duplicate week issues)
        start = (lastDate - dt.timedelta(days=21)).strftime("%Y-%m-%d")

        new = yf.download( tickers=self.symbol, interval="1wk", start=start, end=endDate, progress=False, auto_adjust=False).reset_index()[["Date", "Close"]]

        new["Date"] = pd.to_datetime(new["Date"])

        # 3) merge, dedupe, sort
        merged = pd.concat([old[["Date", "Close"]], new], ignore_index=True)
        merged = merged.drop_duplicates(subset=["Date"], keep="last").sort_values("Date")

        # 4) recompute returns
        merged["Return"] = np.log(merged["Close"] / merged["Close"].shift(1)) * 100

        # 5) save back
        merged.to_csv(self.path, index=False)
        print(f"BTC Updated and Saved at {self.path}")

        

#         if os.path.exists(fileName):
#             self.df = pd.read_csv(fileName)
#             return self.df
#         else:
#             self.maxBTC()
#             return self.df

#    # if self.path.exists():
        #     self.df = pd.read_csv(path)
        #     lastDate = self.df.iloc[-1]['Date']
        #     sevenDaysAhead = dt.datetime.strptime(lastDate, "%Y-%m-%d") + dt.timedelta(days=7)
        #     if sevenDaysAhead <= today:
        #         btcReturn = self.df.iloc[-1]['Return']
        #         return btcReturn
        #     else:
        #         return 0
        # else:
        #     return 0

           # def fileExistsOld(self):
    #     fileName = self.path
    #     fileExists = False
    #     if os.path.exists(fileName):
    #         fileExists = True
    #         self.readFile()
    #     else:
    #         self.createFile()