import html
import os

import requests
from datetime import date, timedelta
from twilio.rest import Client

TWILIO_ACCOUNT_SID = "ACfcef4c014cb22a8669b2520e79812bc5"
TWILIO_AUTH_TOKEN = "76c05e412b7aa289b5c5613ed81d759b"
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_KEY = "a8353661650445f6a795ee014e8b16c1"
NEWS_PARAM = {
    "qInTitle": COMPANY_NAME,
    "searchIn": "title,description",
    "apikey": NEWS_KEY
}

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_KEY = "A0V5342IWC4OR5YN"
STOCK_PARAMS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_KEY
}



""" 
STEP 1: Use https://newsapi.org/docs/endpoints/everything
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
#HINT 1: Get the closing price for yesterday and the day before yesterday. Find the positive difference between the two 
prices. e.g. 40 - 20 = -20, but the positive difference is 20.
#HINT 2: Work out the value of 5% of yesterday's closing stock price.
"""
stock_response = requests.get(url=STOCK_ENDPOINT, params=STOCK_PARAMS)
stock_response.raise_for_status()
stock_data = stock_response.json()["Time Series (Daily)"]
stock_data_list = [value for (key, value) in stock_data.items()]

yesterday_closing_price = stock_data_list[0]["4. close"]
day_before_yesterday_closing_price = stock_data_list[1]['4. close']

difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = round((difference / float(yesterday_closing_price)) * 100)

if abs(diff_percent) > 5:
    """
    STEP 2: Use https://newsapi.org/docs/endpoints/everything
    Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME.
    HINT 1: Think about using the Python Slice Operator
    """
    news_response = requests.get(url=NEWS_ENDPOINT, params=NEWS_PARAM)
    news_response.raise_for_status()
    news_data = news_response.json()
    articles = news_data["articles"][:3]

    """
    STEP 3: Use twilio.com/docs/sms/quickstart/python
    Send a separate message with each article's title and description to your phone number.
    HINT 1: Consider using a List Comprehension.
    """
    news_list = [f"{STOCK}: {up_down}{diff_percent}%\nHeadline: {article['title']}.\nBrief: {article['description']}" for article in articles]

    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    for news in news_list:
        message = client.messages \
            .create(
                body=f"{STOCK}: {news}",
                from_='+17123509328',
                to='+917974846611'
                )
        print(message.status)

    # Optional: Format the SMS message like this:
    """
    TSLA: 🔺2%
    Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
    Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
    or
    "TSLA: 🔻5%
    Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
    Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file
    by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
    """
