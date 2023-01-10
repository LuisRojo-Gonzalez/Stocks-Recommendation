from math import log, sqrt, exp
from scipy.stats import norm

"""
This function implements the Black-Scholes formula to value a European stock option, where:
    - C: Fair value
    - N(): normal cdf
    - S: Current stock price
    - K: Strike price (price to buy or sell the option)
    - r: risk-free interest rate
    - T: maturity time
    - sigma: volatility of the asset
"""

def d1(S, K, T, r, sigma):
    return(log(S/K) + (r + (sigma**2 / 2)) * T) / (sigma * sqrt(T))

def d2(S, K, T, r, sigma):
    return d1(S, K, T, r, sigma) - sigma * sqrt(T)

def bs_call(S, K, T, r, sigma):
    return S * norm.cdf(d1(S, K, T, r, sigma)) - K * exp(-r*T) * norm.cdf(d2(S, K, T, r, sigma))
  
def bs_put(S, K, T, r, sigma):
    return K * exp(-r*T) - S * bs_call(S, K, T, r, sigma)