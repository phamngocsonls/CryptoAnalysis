# My fork for Binance Bot
* Get top 18 coin strong buy from top 100 coin
* Blacklist DOGE,SHIB,USD*
* To install: pip3 install -r requirements.txt, replace your coinmarketcap API in main.py "API_KEY"
* To run: python3 main.py (Wait 2 min)

more update: https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc
https://api.coingecko.com/api/v3/coins/categories

# Crypto analysis

Execution time for for 100 crypto currencies that they had a positive changes in the last 1h, 24h, 7days and volume change.
then program make OscMa analysis for the those cryptos and generate four lists(buy, sell, strong_buy and strong_sell)

## Discription:
simple streamlit(screener) app to make MMA and OSC analysis for cryptocurrencies, and gives resaults for which coins are best to buy or sell depending on the interval you using.

#### More about tradingview : https://pypi.org/project/tradingview-ta/

**Stage 0:**
    get a list of lastest active coins in the market (coinmarketcap)

**Stage 1:**
    (tradingView analysis)MA analysis that they have been > 0 the last 1 hour , 24 hours and 7 days and output:
- strong_buy
- buy
- sell
- strong_sell

**Stage 2:**
    OSC analysis on the "strong_buy list" that we got from the analysis in earlier stage and generate: 
- recommanded_list
        

Stage 1 and 2 can be done in different time intervals:
- 1 minute
- 5 minutes
- 15 minutes
- 1 hour
- 4 hours
- 1 day
- 1 week
- 1 month

**Stage 3:**

## Setup:
1.install requierments:
```
pip install -r requirements.txt
```

2. Coinmarketcap API-key

![image](https://user-images.githubusercontent.com/17545900/116851923-a6df8080-abf3-11eb-9ad2-66b6aa6e3667.png)

Docs: https://coinmarketcap.com/api/documentation/v1/

paste your key in main.py -> :

```
def get_marketCap(self):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
    'start':'1',
    'limit':'100', # how many coins to analysis : first 100
    'convert':'USDT' #change the bridge to see other values like BUSD
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'add your key in here',   
    }
```

3. run the program
```
streamlit run main.py
```
=======
        Stage 1,2 can be done in different time intervals:
            1 minute
            5 minutes
            15 minutes
            1 hour
            4 hours
            1 day
            1 week
            1 month
        Stage 3: save the generated Coin_list

# setup:
        1- install requierments:
                pip install -r requirements.txt

        2- coinmarketcap API-key
![image](https://user-images.githubusercontent.com/17545900/116851923-a6df8080-abf3-11eb-9ad2-66b6aa6e3667.png)

                docs: https://coinmarketcap.com/api/documentation/v1/

                set your key as an environment variable with key X-CMC_PRO_API_KEY

        3- run the program
                streamlit run main.py
![image]("https://user-images.githubusercontent.com/17545900/143775971-30f111ca-757b-4727-bbb0-611248201de9.png)

![image](https://user-images.githubusercontent.com/17545900/143775894-4c047f9d-54d3-4a4c-a743-8b0ff9ce3126.png)

