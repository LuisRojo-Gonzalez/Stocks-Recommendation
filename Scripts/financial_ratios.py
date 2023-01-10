import pandas as pd
from yahoofinancials import YahooFinancials
from datetime import date
import numpy as np

"""
This script contains the way we retrieve key statistics of a certain stock, such that further analysis
can be made. In particular, we work with ratios from the balance sheet of the company.
"""

def growth_rate(data):
    rate = (np.log(data.astype(float)) - np.log(data.astype(float).shift(-1))).dropna().mean()

    return rate

def ratios(stock):
    stock_data = YahooFinancials(stock)
    
    statistics = pd.DataFrame.from_dict(stock_data.get_key_statistics_data().values()).T
    
    # get key indicators for assessment
    key_statistics = statistics.loc[["priceToBook", "beta", "bookValue", "trailingEps", "forwardEps", "pegRatio"]]
    
    key_statistics.loc["currentPrice"] = stock_data.get_current_price()
    key_statistics.loc["trailingPER"] = key_statistics.loc["currentPrice"] / key_statistics.loc["trailingEps"][0]
    key_statistics.loc["per"] = stock_data.get_pe_ratio()
    key_statistics.loc["eps"] = stock_data.get_earnings_per_share()
    key_statistics.loc["forwardPER"] = key_statistics.loc["currentPrice"] / key_statistics.loc["forwardEps"][0]

    # it reports last four statements
    cash_statement = pd.DataFrame()
    income_statement = pd.DataFrame()
    balance_statement = pd.DataFrame()

    for i in range(4):
        cash_statement[str(date.today().year - i - 1)] = pd.DataFrame.from_dict(list(stock_data.get_financial_stmts('annual', 'cash')["cashflowStatementHistory"].values())[0][i].values()).T
        income_statement[str(date.today().year - i - 1)] = pd.DataFrame.from_dict(list(stock_data.get_financial_stmts('annual', 'income')["incomeStatementHistory"].values())[0][i].values()).T
        balance_statement[str(date.today().year - i - 1)] = pd.DataFrame.from_dict(list(stock_data.get_financial_stmts('annual', 'balance')["balanceSheetHistory"].values())[0][i].values()).T
    
    key_statistics.loc["growth"] = growth_rate(income_statement.loc["totalRevenue"])
    
    # # compute the free cash flow
    # FreeCashFlow = cash_statement.loc["changeToOperatingActivities"] - cash_statement.loc["capitalExpenditures"]
    # FreeCashFlow_growth = growth_rate(FreeCashFlow)
    # FreeCashFlow_10Y = FreeCashFlow
    
    return key_statistics

# stock_data = YahooFinancials("aapl")

# # it reports last four statements
# cash_statement = pd.DataFrame()
# income_statement = pd.DataFrame()
# balance_statement = pd.DataFrame()

# for i in range(4):
#     cash_statement[str(date.today().year - i - 1)] = pd.DataFrame.from_dict(list(stock_data.get_financial_stmts('annual', 'cash')["cashflowStatementHistory"].values())[0][i].values()).T
#     income_statement[str(date.today().year - i - 1)] = pd.DataFrame.from_dict(list(stock_data.get_financial_stmts('annual', 'income')["incomeStatementHistory"].values())[0][i].values()).T
#     balance_statement[str(date.today().year - i - 1)] = pd.DataFrame.from_dict(list(stock_data.get_financial_stmts('annual', 'balance')["balanceSheetHistory"].values())[0][i].values()).T

# # company's equity
# equity = balance_statement.loc["totalAssets"] - balance_statement.loc["totalLiab"]

# # residual income
# # return = 0.05

# D = stock_data.get_dividend_rate()#*stock_data.get_current_price()
# r = 

# operating_assets = balance_statement.loc["cash"] + 
# residual_income = income_statement.loc["operatingIncome"] - 0.05 * 