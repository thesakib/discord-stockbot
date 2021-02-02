import requests
import json

list = ['AAPL', 'INO', 'AMD']

for symbol in list:
    # print(symbol)
    website = "https://finnhub.io/api/v1/quote?symbol=" + symbol + "&token=c0c3a6f48v6o915a1bl0"
    # print(website)
    r = requests.get(website)

    data = r.json()
    # print(data)

    print(data["c"])
