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

    def stockprice(self):
        today = datetime.date.today()
        last_week = today - datetime.timedelta(days=7)

        stock_data = yf.download(self.ticker, start=last_week, end=today)
        stock_data.reset_index(inplace=True)

        columns = stock_data.columns
        stockprice_data = {}
        for i in range (0,5):
            for j in columns:
                stockprice_data[j] = stock_data[j][i]

        return stockprice_data

    def finmetric(self):
        ticker = yf.Ticker(self.ticker)

        financials = ticker.financials
        income_stmt = ticker.income_stmt
        dividends = ticker.dividends


        if financials.empty or income_stmt.empty:
            print("Financials or income statement data is not available.")
            return

        latest_financials = financials.iloc[:, 0] 
        latest_income = income_stmt.iloc[:, 0] 

        latest_dividend = dividends.iloc[-1] if not dividends.empty else 0  

        finmetric_data = {
            "quarter": latest_income.name.strftime('%Y-%m-%d'), 
            "revenue": latest_financials['Total Revenue'],
            "earnings": latest_income['Net Income'],
            "dividends": latest_dividend
        }

        return finmetric_data  
    
    def news(self):
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)

        today_str = today.strftime('%Y-%m-%d')
        yesterday_str = yesterday.strftime('%Y-%m-%d')

        query = f"{self.ticker} stock"  
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
                print(result)
                stock_news_data.append(result)
        else:
            print("No news articles available.")
        
        return stock_news_data
    
# ticker = yf.Ticker("AAPL")

# info = ticker.info

# print(ticker.recommendations)
# print(ticker.analyst_price_targets)



# sd = stockdata("AAPL")
# sd.ecoindicator()