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
    buy = 0
    sell = 0
    indicator = 0 # how many indicators to use
    incomplete = 0
    
    indicator = indicator + 1
    if not np.isnan(stock_ratios.loc["enterpriseToEbitda"][0]):
        if stock_ratios.loc["enterpriseToEbitda"][0] < 10:
            # print("Balance seems to be healthy")
            buy = buy + 1
        else:
            sell = sell + 1
    else:
        incomplete = incomplete + 1
    
    indicator = indicator + 1
    if not np.isnan(stock_ratios.loc["trailingPER"][0]) and not np.isnan(stock_ratios.loc["forwardPER"][0]):
        if stock_ratios.loc["trailingPER"][0] > stock_ratios.loc["forwardPER"][0]:
            # print("Earnings are expeted to increase")
            buy = buy + 1
        else:
            sell = sell + 1
    else:
        incomplete = incomplete + 1
    
    indicator = indicator + 1
    if not np.isnan(stock_ratios.loc["pegRatio"][0]):
        if (0 < stock_ratios.loc["pegRatio"][0]) and (stock_ratios.loc["pegRatio"][0] < 1):
            # print("Company seems to be undervalued in comparison to the future")
            buy = buy + 1
        else:
            sell = sell + 1
    else:
        incomplete = incomplete + 1
    
    indicator = indicator + 1
    if not np.isnan(stock_ratios.loc["currentPrice"][0]) and not np.isnan(stock_ratios.loc["bookValue"][0]):
        if stock_ratios.loc["currentPrice"][0] < stock_ratios.loc["bookValue"][0]:
            # print("Company seems to be undervalued")
            buy = buy + 1
        else:
            sell = sell + 1
    else:
        incomplete = incomplete + 1
    
    indicator = indicator + 1
    if not np.isnan(stock_ratios.loc["priceToBook"][0]):
        if stock_ratios.loc["priceToBook"][0] < 1:
            # print("Stock seems to be a solid investment currently")
            buy = buy + 1
        else:
            sell = sell + 1
    else:
        incomplete = incomplete + 1

    return buy / (buy + sell), sell / (buy + sell), incomplete / indicator

def stock_indicators(stock):
    key_indicators = ratios(stock)
    values = [GrahamValue(key_indicators), GrahamNumber(key_indicators), FMAValue(key_indicators)]
    
    intrinsic_value = mean_intrinsic_value(values)
    margin = security_margin(intrinsic_value, key_indicators)
    buy, sell, incomplete = score(key_indicators)
    
    result = {'Stock': stock,
              'CurrentPrice': key_indicators.loc["currentPrice"][0],
              'IntrinsicValue': intrinsic_value,
              'SafetyMargin': margin,
              'BuyScore': buy,
              'SellScore': sell,
              'IncompleteInformation': incomplete}
    
    return result

def stock_analysis(tickers):
    
    """
    This function uses multiprocess to compute the indicators over several tickers and returns a dataframe,
    such that all the results are shown.
    """
    
    with Pool(multiprocessing.cpu_count() - 1) as p:
        indicators = pd.DataFrame.from_dict(list(p.map(stock_indicators, tickers))).set_index('Stock')
    
    return indicators