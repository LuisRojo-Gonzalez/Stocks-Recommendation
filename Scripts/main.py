from Scripts.analysis import stock_analysis
import time

tickers = ["AAPL", "VNTR", "AMZN", "TSLA"]

start = time.time()
stock_analysis(tickers)
print(time.time() - start)