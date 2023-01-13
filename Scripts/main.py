from Scripts.analysis import stock_analysis

tickers = ["CGC", "VNTR", "DOLE", "ET", "BLCM", "SNDL", "GOOGL", "ALLK", "META", "AMC", "SGML",
           "NRGV", "TELL", "GOEV", "AMZN", "GTLB", "AI", "TSLA", "LICY", "MSFT", "ACB",
           "GEVO", "MELI", "CSIQ", "AAL", "INTC", "DIS", "SBUX",
           "NVDA", "KO", "NFLX", "T", "PG", "DDL"]

results = stock_analysis(tickers)

results.query("CurrentPrice < IntrinsicValue and BuyScore >= SellScore")