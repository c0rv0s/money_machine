# script to calculate ultimate MA indicator and then report results to telegram

import math, time, schedule
import requests
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from datetime import datetime

def telegram_bot_sendtext(bot_message):
    
    bot_token = '832441474:AAGeWzau9CZxInYkFmislgmnrK0vj8GzNGw'
    chat_id = '-1001407136445'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + chat_id + '&parse_mode=Markdown&text=' + bot_message
    
    response = requests.get(send_text)
    
    return response.json()


#request data from crypto compare
# t= histohour
# t = histoday
def fetch_data(length, time, sym):
    #only use volumeto (dollars)
    length = str(length)
    api_uri = 'https://min-api.cryptocompare.com/data/'+time+'?fsym='+sym+'&tsym=USD&limit='+length+'&e=Kraken&api_key=fa05711eb31df6703c13a4672a8e84b65948dcb2f142a1f81b0c23b3dee57603'
    
    d = requests.get(api_uri).json()['Data']

    volume = []
    close = []
    time = []
    for entry in d:
        volume.append(entry['volumeto'])
        close.append(entry['close'])
        time.append(entry['time'])
    return volume, close, time

#full analysis method
def job(sym, tframe):
    #get data
    length= 1000
    volume, close, time = fetch_data(length, tframe,sym)
    data = {'close': close}
    df = pd.DataFrame(data)
    
    '''
    rolling_mean50 = df.close.rolling(window=50).mean()
    rolling_mean99 = df.close.rolling(window=99).mean()
    rolling_mean200 = df.close.rolling(window=200).mean()
    
    for i in range(1,1000):
        if rolling_mean50[i-1] < rolling_mean99[i-1] and rolling_mean50[i] > rolling_mean99[i]:
            print("bullish cross at %d" %i)
    
    plt.plot(df.close, label="XBT Price")
    plt.plot(rolling_mean50, label='XBT 50 Day SMA', color='magenta')
    plt.plot(rolling_mean99, label='XBT 99 Day SMA', color='orange')
    plt.plot(rolling_mean200, label='XBT 200 Day SMA', color='green')
    plt.legend(loc='upper left')
    plt.show()
    '''
    
    exp50 = df.close.ewm(span=50, adjust=False).mean()
    exp99 = df.close.ewm(span=99, adjust=False).mean()
    
    crossings = {'bear': [], 'bull': []}
    for i in range(1,length+1):
        if exp50[i-1] < exp99[i-1] and exp50[i] > exp99[i]:
            crossings['bull'].append("bullish cross on %s %s at %s, price is %d" % (sym, tframe[5:], datetime.fromtimestamp(time[i]), df.close[i]))
            #print(crossings['bull'][-1], i)
            if i == 1000:
                return crossings['bull'][-1]
        elif exp50[i-1] > exp99[i-1] and exp50[i] < exp99[i]:
            crossings['bear'].append("bearish cross on %s %s at %s, price is %d" % (sym, tframe[5:], datetime.fromtimestamp(time[i]), df.close[i]))
            #print(crossings['bear'][-1], i)
            if i == 1000:
                return crossings['bear'][-1]
    
    '''
    plt.plot(df.close, label=sym+' Price')
    plt.plot(exp50, label=sym+' 50 EMA')
    plt.plot(exp99, label=sym+' 99 EMA')
    plt.legend(loc='upper left')
    plt.show()
    '''
    return False

def runhour():
    v = job('BTC', 'histohour')
    if v:
        telegram_bot_sendtext(v)

def runday():
    v = job('BTC', 'histoday')
    if v:
        telegram_bot_sendtext(v)

#main/scheduling
schedule.every().hour.do(runhour)
schedule.every().day.at("00:00").do(runday)
while True:
    schedule.run_pending()
    time.sleep(1)

