# script to calculate ultimate MA indicator and then report results to telegram

import math
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

from utils import convert
from config import *

#full analysis method
def mm_job(sym, tframe, data, backtest, shorts=True, longs=True):
    len1 = 20
    a=0.7
    smoothe = 1 #1 to 10

    #get data
    length= len(data)
    volume, close, open, time = convert(data)
    data = {'date': time, 'close': close, 'open': open, 'volume': volume}
    df = pd.DataFrame(data)
    df.columns = ['date', 'close', 'open', 'volume']

    #moving averages
    ema1 = df.close.ewm(span=len1, adjust=False).mean()
    hullma = ((2*(df.close.ewm(span=len1/2, adjust=False).mean()))-ema1).ewm(span=math.sqrt(len1), adjust=False).mean()

    #testing trading
    balance = 100.0
    openingb = balance
    trade = False
    topen = 0.0
    vals = []
    #we are going to use the hullma
    direction = 'none'
    change = False
    for i in range(smoothe,length):
        change = False
        if hullma[i] >= hullma[i - smoothe] and direction != 'up':
            direction = 'up'
            change = True

            if backtest:
                if i > 900:
                    print('new direction is up, '+str(datetime.fromtimestamp(time[i]))+' $'+str(close[i]))
                
                if trade and shorts:
                    amount = (balance * (topen / close[i])) - balance
                    balance += (amount*leverage)*0.9974
                print('bought at '+str(close[i])+' '+ str(datetime.fromtimestamp(time[i]))+' new balance: '+str(balance))
                topen = close[i]
                trade = True
                
        if hullma[i] < hullma[i - smoothe] and direction != 'down':
            direction = 'down'
            change = True
            
            if backtest:
                if i > 900:
                    print('new direction is down, '+str(datetime.fromtimestamp(time[i]))+' $'+str(close[i]))
                
                if trade and longs:
                    amount = (balance * (close[i])/topen) - balance
                    balance += (amount*leverage)*0.9974
                print('sold at '+str(close[i])+' '+ str(datetime.fromtimestamp(time[i]))+' new balance: '+str(balance))
                topen = close[i]
                trade = True
            
        if backtest:
            vals.append(balance)
            if i > 990:
                print(hullma[i])

    if backtest:        
        plt.plot(vals)
        plt.show()
    if change:
        return direction
    else:
        return False
