import requests
from twilio.rest import Client


STOCK_API_KEY = "XXXXX"
NEWS_API_KEY = "XXXXXXXXXXXXXX"
account_sid = "XXXXXXXXXXXXXXXXXXXXX"
auth_token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla"

# Dictionary with the parameter for the STOCK_ENDPOINT API
parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}
# Stock API
response = requests.get(STOCK_ENDPOINT, params=parameters)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
# tun dictionary into a list
data_list = [value for (key, value) in data.items()]
yesterday = data_list[0]
yesterday_closing_price = yesterday["4. close"]

# day before yesterday's closing stock price
before_yesterday = data_list[1]
before_yesterday_closing_price = before_yesterday["4. close"]

# Find the positive difference between 1 and 2.
difference = float(yesterday_closing_price) - float(before_yesterday_closing_price)
up_or_down = None
if difference > 0:
    up_or_down = "🔺"
else:
    up_or_down = "🔻"

# percentage difference in price
percentage_difference = round(abs(difference / float(yesterday_closing_price) * 100))
# if percentage_difference is greater than 0
if percentage_difference > 0:
    news_parameters = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    news_data = news_response.json()["articles"]

    # Get three news articles from news_data
    three_articles = news_data[:3]

    # Format a list of the articles
    articles_formatted = [f"{STOCK_NAME}: {up_or_down}{percentage_difference}%\n" \
                          f"Headline: {article['title']}. " \
                          f"\nBrief:{article['description']}" for article in three_articles]

    # Send each article as a separate message via Twilio.
    client = Client(account_sid, auth_token)
    for article in articles_formatted:
        message = client.messages \
            .create(
            body=article,
            from_='+190341XXXXX',
            to='858XXXXXXX'
        )
