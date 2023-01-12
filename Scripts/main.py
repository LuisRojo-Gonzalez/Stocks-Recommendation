from Scripts.analysis import stock_analysis, stock_indicators
import time

tickers = ["CGC", "VNTR", "DOLE", "ET", "BLCM", "SNDL", "GOOGL", "ALLK", "META", "AMC", "SGML",
           "NRGV", "TELL", "GOEV", "AMZN", "GTLB", "AI", "TSLA", "LICY", "MSFT", "ACB",
           "GEVO", "MELI", "CSIQ", "AAL", "INTC", "DIS", "SBUX",
           "NVDA", "KO", "NFLX", "T", "PG", "DDL"]

start = time.time()
stock_analysis(tickers)
print(time.time() - start)