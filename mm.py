# script to calculate ultimate MA indicator and then report results to telegram

import math
import pandas as pd
import numpy as np
from datetime import datetime
#import matplotlib.pyplot as plt

from utils import convert

#globals
len1 = 20
a=0.7
smoothe = 1 #1 to 10

#full analysis method
def mm_job(sym, tframe, data):
    #get data
    length= len(data)
    volume, close, open, time = convert(data)
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
    '''
    #Tilson T3
    ema4 = ema3.ewm(span=len1, adjust=False).mean()
    ema5 = ema4.ewm(span=len1, adjust=False).mean()
    ema6 = ema5.ewm(span=len1, adjust=False).mean()
    c1 = -a**(3)
    c2 = 3 * a**(2) + 3 * a**(3)
    c3 = -6 * a ** (2) - 3 * a - 3 * a ** (3)
    c4 = 1 + 3 * a + a ** (3) + 3 * a ** (2)
    tilT3 = c1*ema6 + c2*ema5 + c3*ema4 + c4*ema3
    '''
    #testing trading
    balance = 100.0
    openingb = balance
    trade = False
    topen = 0.0
    leverage = 3
    vals = []
    #we are going to use the hullma
    direction = 'none'
    change = False
    for i in range(smoothe,length):
        change = False
        if hullma[i] >= hullma[i - smoothe] and direction != 'up':
            direction = 'up'
            change = True
            '''
            if i > 900:
                print('new direction is up, '+str(datetime.fromtimestamp(time[i]))+' $'+str(close[i]))
            
            if trade:
                amount = (balance * (topen / close[i])) - balance
                balance += (amount*leverage)*0.9974
            #print('going long at '+str(close[i])+' '+ str(datetime.fromtimestamp(time[i]))+' new balance: '+str(balance))
            topen = close[i]
            trade = True
            '''
        if hullma[i] < hullma[i - smoothe] and direction != 'down':
            direction = 'down'
            change = True
            '''
            if i > 900:
                print('new direction is down, '+str(datetime.fromtimestamp(time[i]))+' $'+str(close[i]))
            
            if trade:
                amount = (balance * (close[i])/topen) - balance
                balance += (amount*leverage)*0.9974
            #print('going short at '+str(close[i])+' '+ str(datetime.fromtimestamp(time[i]))+' new balance: '+str(balance))
            topen = close[i]
            trade = True
            '''
        #vals.append(balance)
        #if i > 990:
            #print(hullma[i])
                
    #plt.plot(vals)
    #plt.show()
    if change:
        return direction
    else:
        return False
