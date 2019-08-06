# script to calculate ultimate MA indicator and then report results to telegram

import requests, math, time, schedule

#globals
len1 = 20.0
factorT3 = 7.0
atype = 1.0
smoothe = 2.0
len2 = 50.0
sfactorT3 = 7.0
atype2 = 1.0

def telegram_bot_sendtext(bot_message):
    
    bot_token = '832441474:AAGeWzau9CZxInYkFmislgmnrK0vj8GzNGw'
    chat_id = '-1001407136445'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + chat_id + '&parse_mode=Markdown&text=' + bot_message
    
    response = requests.get(send_text)
    
    return response.json()

def nz(x):
    '''
    for i in range(0,len(x)):
        if math.isnan(x[i]):
            x[i] = 0
    '''
    if math.isnan(x):
        return 0.0
    else:
        return x

#old:
#x is closing price list
#y is number of bars to calc over (usually 20)
def wma(x, y):  #weighted moving average
    norm = 0.0
    sum = 0.0
    lenx = len(x)
    for i in range(lenx-y,lenx):
        weight = (y - i) * y
        norm += weight
        sum += x[i] * weight
    return sum / norm

def ema(x):  #expoential weighted moving average
    lenx = len(x)
    alpha = 2 / (y + 1)
    sum = [0.0]
    for i in range(0,lenx):
        sum.append(alpha * x[i] + (1 - alpha) * nz(sum[-1]))
    return sum

def sma(x, y):  #simple moving average
    sum = 0.0
    lenx = len(x)
    for i in range(lenx-y,lenx):
        sum += x[i]
    return sum / y

#volume = current bar volume
def vwma(x, y, volume): #volume weighted moving average
    new_x=[]
    lenx = len(x)
    for i in range(lenx-y,lenx):
        new_x.append(x[i]*volume[i])
    return sma(new_x, y) / sma(volume, y)

def rma(x, y):  #rma
    lenx = len(x)
    alpha = y
    sum = [0.0]
    for i in range(0,lenx):
        sum.append((x[i] + (alpha - 1) * nz(sum[-1])) / alpha)
    return sum[-1]

#custom defs
def gd(src, length, factor):
    ema(src, length) * (1 + factor) - ema(ema(src, length), length) * factor

def t3(src, length, factor):
    gd(gd(gd(src, length, factor), length, factor), length, factor)

def sgd(src, length, sfactor):
    ema(src, length) * (1 + sfactor) - ema(ema(src, length), length) * sfactor

def st3(src, length, sfactor):
    sgd(sgd(gd(src, length, sfactor), length, sfactor), length, sfactor)

#request data from crypto compare
def fetch_data(length):
    #only use volumeto (dollars)
    length = str(length)
    api_uri = 'https://min-api.cryptocompare.com/data/histoday?fsym=BTC&tsym=USD&limit='+length+'&e=Kraken&api_key=fa05711eb31df6703c13a4672a8e84b65948dcb2f142a1f81b0c23b3dee57603'

    d = requests.get(api_uri).json()['Data']
    volume = []
    close = []
    for entry in d:
        volume.append(entry['volumeto'])
        close.append(entry['close'])
    return volume, close

#full analysis method
def job():
    #get data
    volume, close = fetch_data(1000)

    #begin analysis
    #hull ma definition
    hullma = wma(2*wma(close, len1/2)-wma(close, len1), round(sqrt(len1)))
    #TEMA definition
    ema1 = ema(close, len1)
    ema2 = ema(ema1, len1)
    ema3 = ema(ema2, len1)
    tema = 3 * (ema1 - ema2) + ema3
    #Tilson T3
    factor = factorT3 *.10
    tilT3 = t3(close, len1, factor)
    avg = atype == 1 ? sma(close,len1) : atype == 2 ? ema(close,len1) : atype == 3 ? wma(close,len1) : atype == 4 ? hullma : atype == 5 ? vwma(close, len1, volume) : atype == 6 ? rma(close,len1) : atype == 7 ? 3 * (ema1 - ema2) + ema3 : tilT3
    '''
    #optional 2nd ma, not necessary, may play with later
    #2nd Ma - hull ma definition
    hullma2 = wma(2*wma(close, len2/2)-wma(close, len2), round(sqrt(len2)))
    #2nd MA TEMA definition
    sema1 = ema(close, len2)
    sema2 = ema(sema1, len2)
    sema3 = ema(sema2, len2)
    stema = 3 * (sema1 - sema2) + sema3
    #2nd MA Tilson T3
    sfactor = sfactorT3 *.10
    stilT3 = st3(close, len2, sfactor)
    avg2 = atype2 == 1 ? sma(close,len2) : atype2 == 2 ? ema(close,len2) : atype2 == 3 ? wma(close,len2) : atype2 == 4 ? hullma2 : atype2 == 5 ? vwma(close, len2, volume) : atype2 == 6 ? rma(close,len2) : atype2 == 7 ? 3 * (ema1 - ema2) + ema3 : stilT3
    '''
    #Formula for Price Crossing Moving Average #1
    #this is where i stopped - line 69(lol, nice)


#main/scheduling
'''
schedule.every(8).hours.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
'''
