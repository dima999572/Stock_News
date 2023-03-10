import requests
import datetime as dt
import vonage

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

url_alphavantage = "https://www.alphavantage.co/query"
params_alphavantage = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": "TSLA",
    "apikey": os.environ["ALPHAVANTAGE_API_KEY"]
}


response_alphavantage = requests.get(url=url_alphavantage, params=params_alphavantage)
# Or to get yesterday and day before yesterday I can use comprehension
yesterday = f"{(dt.datetime.today() - dt.timedelta(days=1)).strftime('%Y-%m-%d')}"
day_before_yesterday = f"{(dt.datetime.today() - dt.timedelta(days=2)).strftime('%Y-%m-%d')}"
yesterday_data = float(response_alphavantage.json()["Time Series (Daily)"][yesterday]["4. close"])
day_before_yesterday_data = float(response_alphavantage.json()["Time Series (Daily)"][day_before_yesterday]["4. close"])
average = ((yesterday_data + day_before_yesterday_data) / 2)
percentage = round(((yesterday_data - day_before_yesterday_data) / average) * 100, 2)
 

url_news_api = "https://newsapi.org/v2/everything?"
params_news_api = {
    "q": "TSLA",
    "from": yesterday_data,
    "sortBy": "popularity",
    "apiKey": os.environ["NEWS_API_KEY"]
}

response_news_api = requests.get(url=url_news_api, params=params_news_api)
news = response_news_api.json()["articles"][0:3]

if percentage <= -2 or percentage >= 2:
    if percentage > 0:
        message = [f"TSLA: grow {abs(percentage)}\nHeadline: {data['title']}\nBrief: {data['description']}" for data in
                   news]
    else:
        message = [f"TSLA: drop {abs(percentage)}\nHeadline: {data['title']}\nBrief: {data['description']}" for data in
                   news]
else:
    print("No any news")



if message is not None:
    end_message = ""

    for data in message:
        end_message += data + "\n\n"

    client = vonage.Client(key=os.environ["VONAGE_API_KEY"], secret=os.environ["VONAGE_API_SECRET"])
    sms = vonage.Sms(client)

    print(end_message)

    response_data = sms.send_message({
        "from": "Vonage APIs",
        "to": os.environ["MY_NUMBER"],
        "text": end_message
    }
    )

