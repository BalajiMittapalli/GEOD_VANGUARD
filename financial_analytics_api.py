import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime
import os
from data_pull import StockDataPuller

# Import math functions from assets folder
from assets.mdd import calculate_drawdown_analysis, calculate_max_drawdown
from assets.wacc import (
    calculate_market_return, calculate_cost_of_equity, calculate_cost_of_debt, 
    calculate_wacc, calculate_unlevered_beta, calculate_levered_beta
)

app = FastAPI(title="Financial Analytics API", version="1.0.0")

# Pydantic Models
class AnalyticsRequest(BaseModel):
    ticker: str
    start_date: str
    end_date: str

class AnalyticsResponse(BaseModel):
    ticker: str
    max_drawdown: float
    beta: float
    unlevered_beta: float
    optimal_wacc: float
    optimal_debt_ratio: float
    monthly_return: List[float]
    drawdown_curve: List[float]
    rebase_curve: List[float]
    wacc_curve: List[Dict[str, float]]

# Data pull wrapper function
def datapull(ticker: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
    """
    Wrapper function for data pulling that returns DataFrame with close column
    """
    API_KEY = os.getenv('TWELVE_DATA_API_KEY', "28633be741c54cedba797cd8298f24c8")
    puller = StockDataPuller(API_KEY)
    
    try:
        # Use the existing get_monthly_data method
        df = puller.get_monthly_data(ticker)
        if df is None:
            raise ValueError(f"No data returned for ticker {ticker}")
        
        # Rename 'close' column if it exists with different name
        if 'close' not in df.columns:
            # Check for common close price column names
            close_cols = [col for col in df.columns if 'close' in col.lower()]
            if close_cols:
                df = df.rename(columns={close_cols[0]: 'close'})
            else:
                raise ValueError(f"No close price column found for {ticker}")
        
        # Filter by date range if provided
        if start_date or end_date:
            df['datetime'] = pd.to_datetime(df['datetime'])
            if start_date:
                df = df[df['datetime'] >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df['datetime'] <= pd.to_datetime(end_date)]
        
        return df.sort_values('datetime').reset_index(drop=True)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data for {ticker}: {str(e)}")

# Financial Analytics Functions - Using functions from assets folder
def compute_monthly_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert price data to monthly frequency and compute returns
    Note: When we have Dec 2019 data, Jan 2020 return should be calculated properly.
    The pct_change() method will create NaN for the first row, so we handle this case.
    """
    df = df.copy()
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index('datetime', inplace=True)
    monthly_df = df.resample('M').last()
    
    # Calculate monthly returns using pct_change
    monthly_df['monthly_return'] = monthly_df['close'].pct_change()
    
    # Reset index to get datetime back as a column
    result_df = monthly_df.reset_index()
    
    # The key insight: pct_change() creates NaN for the first row because there's no previous row
    # But if our data starts with Dec 2019 and includes Jan 2020, the Jan 2020 return calculation
    # should work. The issue is we're getting NaN for the first calculation.
    
    # If the first row has NaN and we have at least 2 data points, 
    # then pct_change worked correctly but first return can't be calculated
    # This is expected behavior - we either:
    # 1. Keep the NaN (indicating no previous data for first period)
    # 2. Or drop the first row if we want only valid returns
    
    # For financial analysis, it's common to drop the first NaN return
    # since you need a previous period to calculate a return
    result_df = result_df.dropna(subset=['monthly_return'])
    
    return result_df

def compute_max_drawdown(df: pd.DataFrame) -> tuple:
    """
    Compute maximum drawdown using assets/mdd.py functions
    """
    # Use the calculate_drawdown_analysis function from assets/mdd.py
    analysis_df = calculate_drawdown_analysis(df['close'])
    
    # Extract the required columns and rename to match expected format
    df = df.copy()
    df['monthly_return'] = analysis_df['Return'] / 100  # Convert from percentage to decimal
    df['rebase_100'] = analysis_df['Rebase']
    df['rolling_max'] = analysis_df['Peak']
    df['drawdown'] = analysis_df['Drawdown'] / 100  # Convert from percentage to decimal
    
    # Get maximum drawdown using the assets function (keep as percentage)
    max_drawdown = calculate_max_drawdown(analysis_df['Drawdown'])  # Keep as percentage
    
    return df, max_drawdown

def compute_beta(stock_df: pd.DataFrame, start_date: str, end_date: str) -> tuple:
    """
    Compute beta against SPY
    """
    # Get SPY data and compute monthly returns
    spy_df = datapull("SPY", start_date, end_date)
    spy_monthly = compute_monthly_returns(spy_df)
    
    # Align stock and SPY returns by date
    stock_df['datetime'] = pd.to_datetime(stock_df['datetime'])
    spy_monthly['datetime'] = pd.to_datetime(spy_monthly['datetime'])
    
    merged = pd.merge(stock_df[['datetime', 'monthly_return']], 
                     spy_monthly[['datetime', 'monthly_return']], 
                     on='datetime', suffixes=('_stock', '_spy'))
    merged = merged.dropna()
    
    if len(merged) < 2:
        raise ValueError("Insufficient data to compute beta")
    
    # Calculate beta using covariance/variance
    covariance = np.cov(merged['monthly_return_stock'], merged['monthly_return_spy'])[0, 1]
    spy_variance = np.var(merged['monthly_return_spy'])
    beta = covariance / spy_variance if spy_variance != 0 else 0
    
    return beta, merged['monthly_return_spy']

def compute_unlevered_beta(beta: float, ticker: str) -> float:
    """
    Compute unlevered beta using assets/wacc.py function
    """
    # Company-specific D/E ratios for 2024 end
    de_ratios = {"MSFT": 0.25, "NFLX": 0.63}
    de_ratio = de_ratios.get(ticker.upper(), 0.30)
    
    # Calculate equity and debt values based on D/E ratio
    # Assume equity = 1, then debt = de_ratio
    equity_value = 1.0
    debt_value = de_ratio
    
    # Use the calculate_unlevered_beta function from assets/wacc.py
    unlevered_beta = calculate_unlevered_beta(beta, debt_value, equity_value, tax_rate=0.30)
    return unlevered_beta

def compute_wacc_curve(unlevered_beta: float, spy_returns: pd.Series) -> tuple:
    """
    Compute WACC curve using assets/wacc.py functions
    """
    risk_free_rate = 0.04
    
    # Calculate market return using assets/wacc.py function
    spy_returns_clean = spy_returns.dropna()
    if len(spy_returns_clean) > 0:
        market_return = calculate_market_return(spy_returns_clean) / 100  # Convert from percentage
    else:
        market_return = 0.10  # Default 10%
    
    wacc_data = []
    debt_ratios = np.arange(0.0, 1.00, 0.01)  # 0% to 99% in 1% steps
    
    for debt_ratio in debt_ratios:
        equity_ratio = 1 - debt_ratio
        
        if equity_ratio == 0:
            continue
        
        # Calculate values assuming total value = 1
        debt_value = debt_ratio
        equity_value = equity_ratio
        
        # Calculate relevered beta using assets/wacc.py
        relevered_beta = calculate_levered_beta(unlevered_beta, debt_value, equity_value)
        
        # Calculate cost of equity using assets/wacc.py (pass monthly returns array)
        cost_of_equity = calculate_cost_of_equity(relevered_beta, spy_returns_clean, risk_free_rate)
        
        # Calculate cost of debt using assets/wacc.py
        cost_of_debt = calculate_cost_of_debt(debt_ratio * 100)  # Convert to percentage
        
        # Calculate WACC using assets/wacc.py with tax shield
        wacc = calculate_wacc(equity_value, debt_value, cost_of_equity, cost_of_debt, tax_rate=0.30)
        
        wacc_data.append({
            'debt_ratio': float(debt_ratio),
            'equity_ratio': float(equity_ratio),
            'relevered_beta': float(relevered_beta),
            'cost_of_equity': float(cost_of_equity),
            'wacc': float(wacc)
        })
    
    # Find optimal WACC (minimum)
    if wacc_data:
        optimal_point = min(wacc_data, key=lambda x: x['wacc'])
        optimal_wacc = optimal_point['wacc']
        optimal_debt_ratio = optimal_point['debt_ratio']
    else:
        optimal_wacc = 0.0
        optimal_debt_ratio = 0.0
    
    return wacc_data, optimal_wacc, optimal_debt_ratio

def save_enhanced_csv(df: pd.DataFrame, ticker: str, wacc_data: List[Dict]) -> None:
    """
    Save enhanced CSV with all computed metrics
    """
    # Add WACC curve data as separate columns
    for i, wacc_point in enumerate(wacc_data):
        debt_ratio = wacc_point['debt_ratio']
        df[f'relevered_beta_{int(debt_ratio*100):02d}pct'] = wacc_point['relevered_beta']
        df[f'cost_of_equity_{int(debt_ratio*100):02d}pct'] = wacc_point['cost_of_equity']
        df[f'wacc_{int(debt_ratio*100):02d}pct'] = wacc_point['wacc']
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{ticker}_enhanced_analytics_{timestamp}.csv"
    
    df.to_csv(filename, index=False)
    print(f"Enhanced data saved to {filename}")

@app.post("/analytics/run", response_model=AnalyticsResponse)
async def run_financial_analytics(request: AnalyticsRequest):
    """
    Main endpoint for financial analytics
    """
    try:
        ticker = request.ticker.upper()
        start_date = request.start_date
        end_date = request.end_date
        
        # Step 1: Pull stock data
        stock_df = datapull(ticker, start_date, end_date)
        
        # Step 2: Convert to monthly returns
        monthly_df = compute_monthly_returns(stock_df)
        
        # Step 3: Compute maximum drawdown
        enhanced_df, max_drawdown = compute_max_drawdown(monthly_df)
        
        # Step 4: Compute beta
        beta, spy_returns = compute_beta(enhanced_df, start_date, end_date)
        
        # Step 5: Compute unlevered beta
        unlevered_beta = compute_unlevered_beta(beta, ticker)
        
        # Step 6: Compute WACC curve
        wacc_data, optimal_wacc, optimal_debt_ratio = compute_wacc_curve(unlevered_beta, spy_returns)
        
        # Step 7: Add computed metrics to DataFrame
        enhanced_df['beta'] = beta
        enhanced_df['unlevered_beta'] = unlevered_beta
        
        # Step 8: Save enhanced CSV
        save_enhanced_csv(enhanced_df, ticker, wacc_data)
        
        # Step 9: Prepare response data
        monthly_returns = enhanced_df['monthly_return'].fillna(0).tolist()
        drawdown_curve = enhanced_df['drawdown'].fillna(0).tolist()
        rebase_curve = enhanced_df['rebase_100'].fillna(100).tolist()
        
        response = AnalyticsResponse(
            ticker=ticker,
            max_drawdown=float(abs(max_drawdown)),
            beta=float(beta),
            unlevered_beta=float(unlevered_beta),
            optimal_wacc=float(optimal_wacc),
            optimal_debt_ratio=float(optimal_debt_ratio),
            monthly_return=monthly_returns,
            drawdown_curve=drawdown_curve,
            rebase_curve=rebase_curve,
            wacc_curve=wacc_data
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics computation failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Financial Analytics API",
        "version": "1.0.0",
        "endpoints": {
            "analytics": "/analytics/run (POST)",
            "health": "/health (GET)"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)