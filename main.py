from datetime import datetime
import json
from requests import Session
import requests
from tradingview_ta import *
import concurrent.futures

def get_binance_busd_pair():
    response = requests.get("https://api.binance.com/api/v3/ticker/price").json()

    busd_pairs = []

    for ticker in response:
        symbol = ticker["symbol"]
        if symbol[-4:] == "BUSD":
            busd_pairs.append(symbol[:-4])

    return busd_pairs

class Crypto_analysis:
    
    all=[]
    interval=""
    osc_coins={}
    buy=[]
    sell=[]
    strong_buy=[]
    strong_sell=[]
    recommanded_list=[]
    

    #this method collect the 100 latest cryptocurrency 
    #filtering them by taking only the positive changes in 1h, 24h, 7d, +Vol_24h
    def get_marketCap():
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {
        'start':'1',
        'limit':'100', # you can change this value to get bigger list, but it will effect raise the processing time around 2 min with each 100
        'convert':'BUSD'#bridge coin (btcUSDT) u can change it to BUSD or any bridge
        }
        headers = {
        'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': 'API-KEY-HERE',
        }

        session = Session()
        session.headers.update(headers)

        try:
            changes={}
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            
                
            for d in data.keys():
                if d=="data":
                    for i in data[d]:
                        ticker=i["symbol"]
                        Crypto_analysis.all.append(ticker)
                        proc_1h = i["quote"]["BUSD"]["percent_change_1h"]
                        proc_24h= i["quote"]["BUSD"]["percent_change_24h"]
                        proc_7d = i["quote"]["BUSD"]["percent_change_7d"]
                        vol_ch24h=i["quote"]["BUSD"]["volume_change_24h"]
                        changes[ticker] = [proc_1h,proc_24h ,proc_7d, vol_ch24h]
            
            Crypto_analysis.recommanded_list = [coin for coin in changes.keys() if changes[coin][0] and changes[coin][1]and changes[coin][2]and changes[coin][3]> 0] 
            
        except: 
            pass 
    
    def get_analysis_mma(ticker):
        try:
            ticker_summery = TA_Handler(
                symbol=ticker+"BUSD",
                screener="crypto",
                exchange="binance",
                interval=Crypto_analysis.interval
            )
            
            rec = ticker_summery.get_analysis().moving_averages["RECOMMENDATION"]

            if rec == "SELL": Crypto_analysis.sell.append(ticker)
            if rec == "STRONG_SELL": Crypto_analysis.strong_sell.append(ticker)
            if rec == "BUY": Crypto_analysis.buy.append(ticker)
            if rec == "STRONG_BUY": Crypto_analysis.strong_buy.append(ticker)

        except:
            pass
        
    def get_analysis_osc(ticker):
        try:
            ticker_summery = TA_Handler(
                symbol=ticker+"BUSD",
                screener="crypto",  
                exchange="binance", 
                interval=Crypto_analysis.interval 
            )
            Crypto_analysis.osc_coins[ticker] = ticker_summery.get_analysis().oscillators["RECOMMENDATION"]          
            
        except: 
            pass
    
    def do_analysis():
        with concurrent.futures.ProcessPoolExecutor() as executor:
            Crypto_analysis.interval = "1 week"
            futures = [executor.submit(Crypto_analysis.get_analysis_osc(ticker),) for ticker in Crypto_analysis.all]
            futures = [executor.submit(Crypto_analysis.get_analysis_mma(ticker),) for ticker in Crypto_analysis.osc_coins.keys()]
            output_list = Crypto_analysis.strong_buy

            busd_pair = get_binance_busd_pair()
            black_list = ['SHIB','DOGE','USD','BNB']
            for i in black_list:
                for j in output_list[:]:
                    if j.find(i) > -1 or j not in busd_pair:
                        output_list.remove(j)
            if len(output_list)>18:
                output_list = output_list[:18]
            print(Crypto_analysis.interval,output_list)
            return output_list

def get_24h_change(coin_name):
    url = "https://api.binance.com/api/v1/ticker/24hr?symbol=" + coin_name + "BUSD"
    r = requests.get(url)
    data = r.json()
    return round(float(data['priceChangePercent']),2)


def main():
    Crypto_analysis.get_marketCap()
    top_coin = Crypto_analysis.do_analysis()    
    return top_coin
        
if __name__ == '__main__':
    print("output:",main())
