# script to calculate ultimate MA indicator and then report results to telegram

import math
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

from utils import convert

#globals
len1 = 20
a=0.7
smoothe = 2 #1 to 10

#full analysis method
def mm_job(sym, tframe, data):
    #get data
    length= 1000
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
    '''
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
    '''
    #we are going to use the tema
    direction = 'none'
    markersup = []
    markersdown = []
    for i in range(smoothe,length):
        if tema[i] >= tema[i - smoothe] and direction != 'up':
            #print('new direction is up, '+str(datetime.fromtimestamp(time[i])))
            direction = 'up'
            markersup.append(i)
        if tema[i] < tema[i - smoothe] and direction != 'down':
            #print('new direction is down, '+str(datetime.fromtimestamp(time[i])))
            direction = 'down'
            markersdown.append(i)

    if tema[length] >= tema[length - smoothe] and direction != 'up':
        return('new direction is up, *'+sym+'*, '+tframe[5:]+' '+str(datetime.fromtimestamp(time[length])))
    if tema[length] < tema[length - smoothe] and direction != 'down':
        return('new direction is down, *'+sym+'*, '+tframe[5:]+', '+str(datetime.fromtimestamp(time[length])))

    '''
    #this is kinda messed up in current version
    plt.plot(df.close, label=sym+' Price')
    plt.plot(tema,marker=7, markevery=markersdown)
    plt.plot(tema,marker=6, markevery=markersup)
    plt.legend(loc='upper left')
    plt.show()
    '''
    return False
