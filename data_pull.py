import pandas as pd
from twelvedata import TDClient
from datetime import datetime
import os

class StockDataPuller:
    def __init__(self, api_key):
        """Initialize the Twelve Data client with API key"""
        self.td = TDClient(apikey=api_key)
        self.symbols = ["MSFT", "NFLX", "NVDA"]
    
    def get_monthly_data(self, symbol):
        """Pull monthly data from Dec 2019 to Dec 2024"""
        try:
            ts = self.td.time_series(
                symbol=symbol,
                interval="1month",
                start_date="2019-12-01",
                end_date="2024-12-31",
                outputsize=5000
            )
            
            df = ts.as_pandas()
            df['symbol'] = symbol
            df.reset_index(inplace=True)
            
            # Filter for exact date range
            df['datetime'] = pd.to_datetime(df['datetime'])
            start_filter = pd.Timestamp('2019-12-01')
            end_filter = pd.Timestamp('2024-12-31')
            filtered_data = df[(df['datetime'] >= start_filter) & (df['datetime'] <= end_filter)]
            
            return filtered_data.sort_values('datetime')
            
        except Exception as e:
            print(f"Error fetching data for {symbol}: {str(e)}")
            return None
    
    def pull_data(self):
        """Pull monthly data for all symbols and save individual CSV files"""
        for symbol in self.symbols:
            print(f"Processing {symbol}...")
            data = self.get_monthly_data(symbol)
            
            if data is not None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{symbol}_monthly_2019Dec_2024Dec_{timestamp}.csv"
                data.to_csv(filename, index=False)
                print(f"Saved {symbol} data to {filename} ({len(data)} records)")
            else:
                print(f"Failed to retrieve data for {symbol}")

def main():
    API_KEY = os.getenv('TWELVE_DATA_API_KEY', "28633be741c54cedba797cd8298f24c8")
    
    puller = StockDataPuller(API_KEY)
    print("Fetching monthly data from December 2019 to December 2024")
    puller.pull_data()

if __name__ == "__main__":
    main()