class weeklyBTC(self):
    def __init__(self):
        path = "data/weeklyBTC.csv"
        today = dt.datetime.today().strftime("%Y-%m-%d")
        if self.path.exists():
            self.df = pd.read_csv(path)
            lastDate = self.df.iloc[-1]['Date']
            sevenDaysAhead = dt.datetime.strptime(lastDate, "%Y-%m-%d") + dt.timedelta(days=7)
            if sevenDaysAhead <= today:
                btcReturn = self.df.iloc[-1]['Return']
                return btcReturn
            else:
                return 0
        else:
            return 0
            
    def load_or_download(self):
        fileName = "data/btcWeekly.csv"
        if os.path.exists(fileName):
            self.df = pd.read_csv(fileName)
            return self.df
        else:
            self.maxBTC()
            return self.df
    
    def needs_update(df):
        today = dt.datetime.today().strftime("%Y-%m-%d")
        lastDate = df.iloc[-1]['Date']
        sevenDaysAhead = dt.datetime.strptime(lastDate, "%Y-%m-%d") + dt.timedelta(days=7)
        if sevenDaysAhead <= today:
            return True
        else:
            return False

    def latest_return(df):
        return df.iloc[-1]['Return']
    
    def update_btc_data(self):
        fileName = "data/btcWeekly.csv"
        if os.path.exists(fileName):
            self.df = pd.read_csv(fileName)
            return self.df
        else:
            self.maxBTC()
            return self.df

    def maxBTC(self):
        ticker = yf.Ticker("BTC-USD")
        fileName = "data/btcWeekly.csv"
        btcMaxDownload = ticker.download(tickers=ticker, period="max", interval="1wk")
        btcMaxDownload['Return'] = np.log(btcMaxDownload['Close'].pct_change())
        btcMaxDownload.to_csv(fileName)
        print(f'BTC Max Downloaded and Saved at {fileName}')


