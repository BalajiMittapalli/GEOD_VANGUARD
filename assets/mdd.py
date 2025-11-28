"""
MDD (Maximum Drawdown) Calculation Module

This module provides functions for calculating and analyzing maximum drawdown,
which measures the largest peak-to-trough decline in an investment.
"""

import pandas as pd
import numpy as np
import yfinance as yf


def get_monthly_data(tickers, start, end):
    """
    Download monthly stock price data from Yahoo Finance
    
    Parameters:
    - tickers : str or list
        Stock ticker symbol(s)
    - start : str
        Start date in 'YYYY-MM-DD' format
    - end : str
        End date in 'YYYY-MM-DD' format
    
    Returns:
    - DataFrame or Series : Monthly adjusted closing prices
    """
    print(f"📥 Downloading data for {tickers}...")
    data = yf.download(tickers, start=start, end=end, interval='1mo', progress=False)
    if data is not None:
        data = data['Adj Close']
    return data


def calculate_drawdown_analysis(prices):
    """
    Calculate comprehensive drawdown analysis
    
    Parameters:
    - prices : Series or array-like
        Price series (adjusted closing prices)
    
    Returns:
    - DataFrame : Contains columns for Returns, Rebase, Peak, and Drawdown
        - Return: Percentage returns
        - Rebase: Cumulative returns rebased to 100
        - Peak: Running maximum value
        - Drawdown: Percentage below peak
    """
    df = pd.DataFrame()
    df['Close'] = prices
    df['Return'] = prices.pct_change() * 100
    
    # Rebase to 100
    df['Rebase'] = (1 + prices.pct_change().fillna(0)).cumprod() * 100
    
    # Calculate running peak
    df['Peak'] = df['Rebase'].expanding().max()
    
    # Calculate drawdown percentage
    df['Drawdown'] = ((df['Rebase'] - df['Peak']) / df['Peak']) * 100
    
    return df


def calculate_max_drawdown(drawdown_series):
    """
    Calculate maximum drawdown from drawdown series
    
    Parameters:
    - drawdown_series : Series or array-like
        Series of drawdown values (typically negative)
    
    Returns:
    - float : Maximum drawdown value (typically negative percentage)
    """
    return drawdown_series.min()


def calculate_recovery_time(prices, drawdown_df):
    """
    Calculate how long it takes to recover from maximum drawdown
    
    Parameters:
    - prices : Series
        Price series
    - drawdown_df : DataFrame
        Output from calculate_drawdown_analysis
    
    Returns:
    - dict : Recovery metrics including recovery time and peak-to-recovery period
    """
    # Find the date of maximum drawdown
    mdd_index = drawdown_df['Drawdown'].idxmin()
    mdd_value = drawdown_df['Drawdown'].loc[mdd_index]
    
    # Find when price recovered (crosses above the peak from MDD date)
    peak_value = drawdown_df['Peak'].loc[mdd_index]
    recovery_df = drawdown_df.loc[mdd_index:][drawdown_df['Rebase'] >= peak_value]
    
    recovery_metrics = {
        'mdd_date': mdd_index,
        'mdd_value': mdd_value,
        'peak_before_mdd': peak_value,
        'recovery_date': recovery_df.index[0] if len(recovery_df) > 0 else None,
        'recovery_days': (recovery_df.index[0] - mdd_index).days if len(recovery_df) > 0 else None
    }
    
    return recovery_metrics


# Example usage
if __name__ == "__main__":
    # Example: Download and analyze MSFT
    ticker = "MSFT"
    start_date = "2023-01-01"
    end_date = "2024-12-31"
    
    prices = get_monthly_data(ticker, start_date, end_date)
    analysis = calculate_drawdown_analysis(prices)
    max_dd = calculate_max_drawdown(analysis['Drawdown'])
    
    print(f"\n{ticker} Drawdown Analysis ({start_date} to {end_date})")
    print(f"Maximum Drawdown: {max_dd:.2f}%")
    print(f"\nAnalysis Summary:")
    print(analysis.tail()) 
