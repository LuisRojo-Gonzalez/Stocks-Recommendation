import numpy as np

def security_margin(fair_value, stock_ratios):
    
    if fair_value > stock_ratios.loc["currentPrice"][0]:
        margin = (fair_value - stock_ratios.loc["currentPrice"][0]) / fair_value
    else:
        margin = np.nan
    
    return margin