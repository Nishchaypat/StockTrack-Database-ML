from sql_connect import sql_connector
import requests
import yfinance as yf
import datetime

class stockdata:
    def __init__(self, ticker):
        self.ticker = ticker
        self.news_api = '8950c31b2f2d406ea056828f40160adc'
    def company(self):

        ticker = yf.Ticker(self.ticker)
        info = ticker.info
        name = info.get('longName') 
        sector = info.get('sector')
        industry = info.get('industry')
        description = info.get('longBusinessSummary')
        company_data = {
            "Name" : name,
            "Sector" : sector,
            "Industry" : industry,
            "Description": description
        }
        return company_data

    def stockprice(self, ticker):
        today = datetime.date.today()
        last_week = today - datetime.timedelta(days=7)

        stock_data = yf.download(ticker, start=last_week, end=today)
        stock_data.reset_index(inplace=True)
        stock_data['Date'] = stock_data['Date'].dt.strftime('%Y-%m-%d')
        stockprice_data = []
        stock_data = stock_data.iloc[-1]
        row_data = {
            'Date': stock_data['Date'],
            'Open': stock_data['Open'].item(),   # Convert to float
            'High': stock_data['High'].item(),   # Convert to float
            'Low': stock_data['Low'].item(),     # Convert to float
            'Close': stock_data['Close'].item(), # Convert to float
            'Volume': int(stock_data['Volume'])  # Convert to int
        }
        stockprice_data.append(row_data)

        return stockprice_data

    def finmetric(self, ticker):
        ticker = yf.Ticker(ticker)

        financials = ticker.financials
        income_stmt = ticker.income_stmt
        dividends = ticker.dividends


        if financials.empty or income_stmt.empty:
            print("Financials or income statement data is not available.")
            return

        latest_financials = financials.iloc[:, 0] 
        latest_income = income_stmt.iloc[:, 0] 

        latest_dividend = dividends.iloc[-1].item() if not dividends.empty else 0  

        finmetric_data = {
            "quarter": latest_income.name.strftime('%Y-%m-%d'), 
            "revenue": latest_financials['Total Revenue'],
            "earnings": latest_income['Net Income'],
            "dividends": latest_dividend
        }

        return finmetric_data  
    
    def news(self, ticker):
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)

        today_str = today.strftime('%Y-%m-%d')
        yesterday_str = yesterday.strftime('%Y-%m-%d')

        query = f"{ticker} stock"  
        url = f'https://newsapi.org/v2/everything?q={query}&from={yesterday_str}&to={today_str}&sortBy=popularity&language=en&apiKey={self.news_api}'

        response = requests.get(url)
        news_data = response.json()
        stock_news_data = []
        if news_data['status'] == 'ok' and news_data['articles']:
            for article in news_data['articles'][:3]:  
                result = {
                    "title": article['title'],
                    "content": article['description'],  
                    "published_date": article['publishedAt']
                }
                stock_news_data.append(result)
        else:
            print("No news articles available.")
        
        return stock_news_data
    

class populate_db:

    def __init__(self):
        self.db = sql_connector()

    def company_table(self, ticker):
        company_sd = stockdata(ticker)
        
        company_data = company_sd.company()
        response = self.db.insert_company(str(ticker), company_data["Name"], company_data["Sector"], company_data["Industry"], company_data["Description"])
        print(response)
        self.stock_price_table(str(ticker))

    def stock_price_table(self, ticker):
        company_sd = stockdata(ticker)
        stock_data = company_sd.stockprice(ticker)
        for row in stock_data:
            date = row['Date'] 
            open_price = row['Open']
            high = row['High']
            low = row['Low']
            close = row['Close']
            volume = row['Volume']
            
            self.db.insert_stock_price(str(ticker), date, open_price, high, low, close, volume)
        self.financial_metric_table(str(ticker))

    def financial_metric_table(self, ticker):
        company_sd = stockdata(ticker)
        fin_data = company_sd.finmetric(ticker)
        quarter = fin_data['quarter'] 
        revenue = fin_data['revenue']
        earnings = fin_data['earnings']
        dividends = fin_data['dividends']

        self.db.insert_financial_metric(str(ticker), quarter, revenue, earnings, dividends)
        self.news_table(str(ticker))

    def news_table(self, ticker):
        company_sd = stockdata(ticker)
        
        stock_news_data = company_sd.news(ticker)

        for row in stock_news_data:
            date = row['published_date'] 
            title = row['title']
            content = row['content']
            
            self.db.insert_news_article(str(ticker), title, content, date)

# populate = populate_db()

# companies = [
#     "NVDA", "AMD", "PYPL", "F", "GM", 
#     "SPGI", "AXP", "GS", "BLK", "MS", 
#     "DE", "IBM", "INTU", "ABBV", "ABT", 
#     "BMY", "LLY", "GILD", "MRNA", "REGN", 
#     "LRCX", "MU", "ADSK", "ATVI", "EA", 
#     "DIS", "RCL", "UAL", "DAL", "AAL", 
#     "BKNG", "MAR", "HLT", "KHC", "MO", 
#     "CL", "EL", "TMO", "ISRG", "SYK", 
#     "BDX", "DHR", "PLTR", "SQ", "SHOP", 
#     "ZS", "PANW", "SNOW", "DDOG", "CRWD"
# ]

# for i in companies:
#     try:
#         populate.company_table(i)
#     except:
#         print(i)