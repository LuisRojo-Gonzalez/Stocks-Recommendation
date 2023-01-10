import numpy as np
from Scripts.financial_ratios import *
from yahoofinancials import YahooFinancials

"""
This script contains several method for a stock valuation price. We can use either
    - the Graham number,
    - the Graham value,
    - the Financial metric analysis
"""

# stock_ratios is computed using ratios("stock_symbol")
def GrahamNumber(stock_ratios):
    
    """
    This method is efficient in evaluating the stocks of companies with positive, tangible book value
    and have a growth rate below 10%.
    """
    
    GrahamNumber = np.nan
    
    if stock_ratios.loc["growth"][0] <= 0.1 and stock_ratios.loc["eps"][0] > 0 and stock_ratios.loc["bookValue"][0] > 0:
        GrahamNumber = np.sqrt(22.5 * stock_ratios.loc["eps"][0] * stock_ratios.loc["bookValue"][0])
    
    return GrahamNumber

def GrahamValue(stock_ratios):
    growth_rate = stock_ratios.loc["growth"][0]
    # low growth company
    if growth_rate <= 0:
        BPE = 8.5
    else:
        BPE = 15
    CG = 2
    
    value = stock_ratios.loc["eps"][0] * (BPE + CG * growth_rate) * 4.4 / YahooFinancials("^TNX").get_current_price()

    return value

def FMAValue(stock_ratios):
    
    """
    This method computes the financial metric analysis
    """

    value = 0
    
    if stock_ratios.loc["growth"][0] > 0:
        value = stock_ratios.loc["eps"][0] * (1 + stock_ratios.loc["growth"][0]) * stock_ratios.loc["per"][0]
    else:
        value = np.nan
    
    return value

# ind = ratios("vntr")

# GrahamNumber(ind)
# GrahamValue(ind)
# FMAValue(ind)

# def dcf():
    
#     fcf = 0
    
#     if (cash_statement.loc["changeToOperatingActivities"] > 0) & (cash_statement.loc["capitalExpenditures"] > 0):
#         fcf = cash_statement.loc["changeToOperatingActivities"] - cash_statement.loc["capitalExpenditures"]
#     else:
#         fcf = np.nan
