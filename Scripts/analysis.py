from Scripts.financial_ratios import ratios
from Scripts.stock_valuation import *
from Scripts.average_value import mean_intrinsic_value
from Scripts.security_margin import security_margin
import multiprocessing
from multiprocessing import Pool
import pandas as pd

"""
This script analyzes the financial key indicators to score the stock current price. To call it we have to invoke
the function as score(ratios(stock))
"""

# stock_ratios is computed using ratios("stock_symbol")
def score(stock_ratios):
    
    # initializes the scoring function
    yes = 0
    no = 0
    
    if stock_ratios.loc["trailingPER"][0] > stock_ratios.loc["forwardPER"][0]:
        # print("Earnings are expeted to increase")
        yes = yes + 1
    else:
        no = no + 1
    
    if (0 < stock_ratios.loc["pegRatio"][0]) & (stock_ratios.loc["pegRatio"][0] < 1):
        # print("Company seems to be undervalued in comparison to the future")
        yes = yes + 1
    else:
        no = no + 1
    
    if stock_ratios.loc["currentPrice"][0] < stock_ratios.loc["bookValue"][0]:
        # print("Company seems to be undervalued")
        yes = yes + 1
    else:
        no = no + 1
    
    if stock_ratios.loc["priceToBook"][0] < 1:
        # print("Stock seems to be a solid investment currently")
        yes = yes + 1
    else:
        no = no + 1

    return yes / (yes + no)

def stock_indicators(stock):
    key_indicators = ratios(stock)
    values = [GrahamValue(key_indicators), GrahamNumber(key_indicators), FMAValue(key_indicators)]
    
    intrinsic_value = mean_intrinsic_value(values)
    margin = security_margin(intrinsic_value, key_indicators)
    scoring = score(key_indicators)
    
    result = {'Stock': stock,
              'CurrentPrice': key_indicators.loc["currentPrice"][0],
              'IntrinsicValue': intrinsic_value,
              'SafetyMargin': margin,
              'BuyScore': scoring}
    
    return result

def stock_analysis(tickers):
    
    """
    This function uses multiprocess to compute the indicators over several tickers and returns a dataframe,
    such that all the results are shown.
    """
    
    with Pool(multiprocessing.cpu_count() - 1) as p:
        indicators = pd.DataFrame.from_dict(list(p.map(stock_indicators, tickers))).set_index('Stock')
    
    return indicators