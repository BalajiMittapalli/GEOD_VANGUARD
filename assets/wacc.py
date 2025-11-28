"""
WACC (Weighted Average Cost of Capital) Calculation Module

This module combines cost of equity, cost of debt, and capital structure
to calculate the weighted average cost of capital.
"""

import numpy as np

def calculate_market_return(monthly_returns):
    m = len(monthly_returns)
    total = np.prod(1 + monthly_returns)

    # YOUR EXACT FORMULA: take (12/m)-th root → exponent = m/12
    Rm = (total ** (m / 12) - 1)*100

    return Rm

def calculate_cost_of_equity(beta, monthly_market_returns, risk_free=0.04):
    Rm = calculate_market_return(monthly_market_returns)
    return risk_free +( beta * (Rm - risk_free))


def calculate_cost_of_debt(debt_percentage, tax_rate=0.30):
    """
    Calculate cost of debt (Kd) based on debt leverage
    
    Parameters:
    - debt_percentage : float
        Debt as a percentage of total capital (0-1 or 0-100)
    - tax_rate : float, default 0.30 (30% corporate tax rate)
        Corporate tax rate for tax shield calculation
    
    Returns:
    - float : After-tax Cost of debt as a decimal
    """
    # Normalize input if percentage is 0-100 instead of 0-1
    if debt_percentage > 1:
        debt_percentage = debt_percentage / 100
    
    # Ensure debt_percentage is within valid range
    debt_percentage = max(0, min(1, debt_percentage))
    
    base_kd = 0.04  # Base cost of debt (4%)
    interest_rate = 0.001  # Interest rate spread per unit debt
    
    # Pre-tax cost of debt
    pre_tax_kd = base_kd + (debt_percentage * interest_rate)
    
    # After-tax cost of debt (accounting for tax shield)
    after_tax_kd = pre_tax_kd * (1 - tax_rate)
    
    return after_tax_kd


def calculate_wacc(equity_value, debt_value, cost_of_equity, cost_of_debt, tax_rate=0.30):
    """
    Calculate Weighted Average Cost of Capital (WACC)
    
    Formula:
        WACC = (E/V × Ke) + (D/V × Kd × (1 - Tc))
    
    Where:
    - E = Market value of equity
    - D = Market value of debt
    - V = E + D (Total firm value)
    - Ke = Cost of equity
    - Kd = Cost of debt (pre-tax)
    - Tc = Corporate tax rate
    
    Parameters:
    - equity_value : float
        Market value of equity
    - debt_value : float
        Market value of debt
    - cost_of_equity : float
        Cost of equity (as decimal, e.g., 0.10 for 10%)
    - cost_of_debt : float
        Pre-tax cost of debt (as decimal)
    - tax_rate : float, default 0.30
        Corporate tax rate
    
    Returns:
    - float : WACC as a decimal
    """
    
    total_value = equity_value + debt_value
    
    if total_value == 0:
        return 0
    
    # Weight of equity and debt
    weight_equity = equity_value / total_value
    weight_debt = debt_value / total_value
    
    # WACC calculation with tax shield
    wacc = (weight_equity * cost_of_equity) + (weight_debt * cost_of_debt * (1 - tax_rate))
    
    return wacc


def calculate_unlevered_beta(levered_beta, debt_value, equity_value, tax_rate=0.30):
    """
    Calculate unlevered (asset) beta from levered (equity) beta
    
    Formula:
        βu = βL / [1 + (1 - Tc) × (D/E)]
    
    Parameters:
    - levered_beta : float
        Current levered beta
    - debt_value : float
        Market value of debt
    - equity_value : float
        Market value of equity
    - tax_rate : float, default 0.30
        Corporate tax rate
    
    Returns:
    - float : Unlevered beta
    """
    if equity_value == 0:
        return levered_beta
    
    debt_to_equity = debt_value / equity_value
    unlevered_beta = levered_beta / (1 + (1 - tax_rate) * debt_to_equity)
    
    return unlevered_beta


def calculate_levered_beta(unlevered_beta, debt_value, equity_value, tax_rate=0.30):
    """
    Calculate levered (equity) beta from unlevered (asset) beta
    
    Formula:
        βL = βu × [1 + (1 - Tc) × (D/E)]
    
    Parameters:
    - unlevered_beta : float
        Asset/unlevered beta
    - debt_value : float
        Market value of debt
    - equity_value : float
        Market value of equity
    - tax_rate : float, default 0.30
        Corporate tax rate
    
    Returns:
    - float : Levered beta
    """
    if equity_value == 0:
        return unlevered_beta
    
    debt_to_equity = debt_value / equity_value
    levered_beta = unlevered_beta * (1 + (1 - tax_rate) * debt_to_equity)
    
    return levered_beta


# Example usage
if __name__ == "__main__":
    # Example parameters
    beta = 1.2  # Levered beta
    market_return_value = 0.10  # 10% market return
    risk_free_rate = 0.04  # 4% risk-free rate
    equity_value = 1000  # $1000M equity value
    debt_value = 500  # $500M debt value
    debt_percentage = 33.33  # Debt as % of capital
    
    # Calculate components
    ke = calculate_cost_of_equity(beta, market_return_value, risk_free_rate)
    kd = calculate_cost_of_debt(debt_percentage)
    wacc = calculate_wacc(equity_value, debt_value, ke, kd)
    
    print(f"Cost of Equity (Ke): {ke:.4f} ({ke*100:.2f}%)")
    print(f"After-tax Cost of Debt (Kd): {kd:.4f} ({kd*100:.2f}%)")
    print(f"WACC: {wacc:.4f} ({wacc*100:.2f}%)")
