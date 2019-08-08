# script to calculate ultimate MA indicator and then report results to telegram

import math, time
import requests
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

#globals
len1 = 20
a=0.7
smoothe = 2 #1 to 10

def mm_telegram_bot_sendtext(bot_message):
    
    bot_token = '832441474:AAGeWzau9CZxInYkFmislgmnrK0vj8GzNGw'
    chat_id = '-1001407136445'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + chat_id + '&parse_mode=Markdown&text=' + bot_message
    
    response = requests.get(send_text)
    
    return response.json()

#request data from crypto compare
# t= histohour
# t = histoday
def mm_fetch_data(length, time, sym):
    #only use volumeto (dollars)
    length = str(length)
    api_uri = 'https://min-api.cryptocompare.com/data/'+time+'?fsym='+sym+'&tsym=USD&limit='+length+'&e=Kraken&api_key=fa05711eb31df6703c13a4672a8e84b65948dcb2f142a1f81b0c23b3dee57603'
    
    d = requests.get(api_uri).json()['Data']

    volume = []
    close = []
    open = []
    time = []
    for entry in d:
        volume.append(entry['volumeto'])
        close.append(entry['close'])
        open.append(entry['open'])
        time.append(entry['time'])
    return volume, close, open, time

#full analysis method
def mm_job(sym, tframe):
    #get data
    length= 1000
    volume, close, open, time = mm_fetch_data(length, tframe,sym)
    data = {'date': time, 'close': close, 'open': open, 'volume': volume}
    df = pd.DataFrame(data)
    df.columns = ['date', 'close', 'open', 'volume']

    #begin analysis
    ema1 = df.close.ewm(span=len1, adjust=False).mean()
    ema2 = ema1.ewm(span=len1, adjust=False).mean()
    ema3 = ema2.ewm(span=len1, adjust=False).mean()
    #triple ma
    tema = 3 * (ema1 - ema2) + ema3
    #hull moving average
    hullma = ((2*(df.close.ewm(span=len1/2, adjust=False).mean()))-ema1).ewm(span=math.sqrt(len1), adjust=False).mean()
    #Tilson T3
    ema4 = ema3.ewm(span=len1, adjust=False).mean()
    ema5 = ema4.ewm(span=len1, adjust=False).mean()
    ema6 = ema5.ewm(span=len1, adjust=False).mean()
    c1 = -a**(3)
    c2 = 3 * a**(2) + 3 * a**(3)
    c3 = -6 * a ** (2) - 3 * a - 3 * a ** (3)
    c4 = 1 + 3 * a + a ** (3) + 3 * a ** (2)
    tilT3 = c1*ema6 + c2*ema5 + c3*ema4 + c4*ema3
    
    #we are going to use the hullma
    direction = 'none'
    markersup = []
    markersdown = []
    for i in range(smoothe,length):
        if hullma[i] >= hullma[i - smoothe] and direction != 'up':
            #print('new direction is up, '+str(datetime.fromtimestamp(time[i])))
            direction = 'up'
            markersup.append(i)
        if hullma[i] < hullma[i - smoothe] and direction != 'down':
            #print('new direction is down, '+str(datetime.fromtimestamp(time[i])))
            direction = 'down'
            markersdown.append(i)
    
    if hullma[length] >= hullma[length - smoothe] and direction != 'up':
        return('new direction is up, '+str(datetime.fromtimestamp(time[length])))
    if hullma[length] < hullma[length - smoothe] and direction != 'down':
        return('new direction is down, '+str(datetime.fromtimestamp(time[length])))
    return False
    '''
    plt.plot(df.close, label=sym+' Price')
    plt.plot(hullma,marker=7, markevery=markersdown)
    plt.plot(hullma,marker=6, markevery=markersup)
    plt.legend(loc='upper left')
    plt.show()
    '''

