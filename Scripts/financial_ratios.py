import pandas as pd
from yahoofinancials import YahooFinancials
from datetime import date
import numpy as np

"""
This script contains the way we retrieve key statistics of a certain stock, such that further analysis
can be made. In particular, we work with ratios from the balance sheet of the company.
"""

def growth_rate(revenue):
    
    rate = (np.log(revenue.astype(float)) - np.log(revenue.astype(float).shift(-1))).dropna().mean()

    return rate

def ratios(stock):
    
    stock_data = YahooFinancials(stock)
    
    statistics = pd.DataFrame.from_dict(stock_data.get_key_statistics_data().values()).T
    
    # get key indicators for assessment
    key_statistics = statistics.loc[["priceToBook", "bookValue", "trailingEps", "forwardEps", "pegRatio", "enterpriseToEbitda"]]
    
    key_statistics.fillna(np.nan, inplace = True)
    
    key_statistics.loc["currentPrice"] = stock_data.get_current_price()

    if not (stock_data.get_pe_ratio() is None):
        key_statistics.loc["per"] = stock_data.get_pe_ratio()
    else:
        key_statistics.loc["per"] = np.nan
    
    if not (stock_data.get_earnings_per_share() is None):
        key_statistics.loc["eps"] = stock_data.get_earnings_per_share()
    else:
        key_statistics.loc["eps"] = np.nan

    # it reports last four statements
    cash_statement = pd.DataFrame()
    income_statement = pd.DataFrame()
    balance_statement = pd.DataFrame()

    cash_statement_aux = list(stock_data.get_financial_stmts('annual', 'cash')["cashflowStatementHistory"].values())[0]
    if cash_statement_aux is None:
        cash_statement = pd.DataFrame(data = [np.nan])
    else:
        for i in range(len(cash_statement_aux)):
            cash_statement[str(date.today().year - i - 1)] = pd.DataFrame.from_dict(cash_statement_aux[i].values()).T

    income_statement_aux = list(stock_data.get_financial_stmts('annual', 'income')["incomeStatementHistory"].values())[0]
    if income_statement_aux is None:
        income_statement = pd.DataFrame(data = [np.nan])
    else:
        # print(stock)
        for i in range(len(income_statement_aux)):
            income_statement[str(date.today().year - i - 1)] = pd.DataFrame.from_dict(income_statement_aux[i].values()).T
    
    balance_statement_aux = list(stock_data.get_financial_stmts('annual', 'balance')["balanceSheetHistory"].values())[0]
    if balance_statement_aux is None:
        balance_statement = pd.DataFrame(data = [np.nan])
    else:
        for i in range(len(balance_statement_aux)):
            balance_statement[str(date.today().year - i - 1)] = pd.DataFrame.from_dict(balance_statement_aux[i].values()).T
    
    # compute other indicators
    if not np.isnan(key_statistics.loc["currentPrice"][0]) and not np.isnan(key_statistics.loc["trailingEps"][0]):
        key_statistics.loc["trailingPER"] = key_statistics.loc["currentPrice"][0] / key_statistics.loc["trailingEps"][0]
    else:
        key_statistics.loc["trailingPER"] = np.nan
        
    if not np.isnan(key_statistics.loc["currentPrice"][0]) and not np.isnan(key_statistics.loc["forwardEps"][0]):
        key_statistics.loc["forwardPER"] = key_statistics.loc["currentPrice"] / key_statistics.loc["forwardEps"][0]
    else:
        key_statistics.loc["forwardPER"] = np.nan
    
    if len(income_statement) > 0 and not pd.isnull(income_statement.loc["totalRevenue"]).any() and not (income_statement.loc["totalRevenue"] <= 0).any():
        # print(stock)
        key_statistics.loc["growth"] = growth_rate(income_statement.loc["totalRevenue"])
    else:
        key_statistics.loc["growth"] = np.nan
    
    # # compute the free cash flow
    # FreeCashFlow = cash_statement.loc["changeToOperatingActivities"] - cash_statement.loc["capitalExpenditures"]
    # FreeCashFlow_growth = growth_rate(FreeCashFlow)
    # FreeCashFlow_10Y = FreeCashFlow
    
    return key_statistics

# ratios("VNTR")

# # company's equity
# equity = balance_statement.loc["totalAssets"] - balance_statement.loc["totalLiab"]

# # residual income
# # return = 0.05

# D = stock_data.get_dividend_rate()#*stock_data.get_current_price()
# r = 

# operating_assets = balance_statement.loc["cash"] + 
# residual_income = income_statement.loc["operatingIncome"] - 0.05 * 