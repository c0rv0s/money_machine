# script to calculate ultimate MA indicator and then report results to telegram

import math
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

from utils import convert

#full analysis method
def ma_job(sym, tframe, data):
    #get data
    length= 1000
    volume, close, open, time = convert(data)
    data = {'date': time, 'close': close, 'open': open, 'volume': volume}
    df = pd.DataFrame(data)
    df.columns = ['date', 'close', 'open', 'volume']
    
    ma50 = df.close.rolling(window=50).mean()
    ma99 = df.close.rolling(window=99).mean()
    ma200 = df.close.rolling(window=200).mean()
    
    crossings = {'bear': [], 'bull': []}
    for i in range(1,length+1):
        #50 and 99
        if ma50[i-1] < ma99[i-1] and ma50[i] >= ma99[i]:
            crossings['bull'].append("bullish cross on *%s* %s at %s, price is %d" % (sym, tframe[5:], datetime.fromtimestamp(time[i]), df.close[i]))
            #print(crossings['bull'][-1], i)
            if i == length:
                return crossings['bull'][-1]
        elif ma50[i-1] > ma99[i-1] and ma50[i] <= ma99[i]:
            crossings['bear'].append("bearish cross on *%s* %s at %s, price is %d" % (sym, tframe[5:], datetime.fromtimestamp(time[i]), df.close[i]))
            #print(crossings['bear'][-1], i)
            if i == length:
                return crossings['bear'][-1]
        #50 and 200
        if ma50[i-1] < ma200[i-1] and ma50[i] >= ma200[i]:
            crossings['bull'].append("bullish cross on *%s* %s at %s, price is %d" % (sym, tframe[5:], datetime.fromtimestamp(time[i]), df.close[i]))
            #print(crossings['bull'][-1], i)
            if i == length:
                return crossings['bull'][-1]
        elif ma50[i-1] > ma200[i-1] and ma50[i] <= ma200[i]:
            crossings['bear'].append("bearish cross on *%s* %s at %s, price is %d" % (sym, tframe[5:], datetime.fromtimestamp(time[i]), df.close[i]))
            #print(crossings['bear'][-1], i)
            if i == length:
                return crossings['bear'][-1]
        #99 and 200
        if ma99[i-1] < ma200[i-1] and ma99[i] >= ma200[i]:
            crossings['bull'].append("bullish cross on *%s* %s at %s, price is %d" % (sym, tframe[5:], datetime.fromtimestamp(time[i]), df.close[i]))
            #print(crossings['bull'][-1], i)
            if i == length:
                return crossings['bull'][-1]
        elif ma99[i-1] > ma200[i-1] and ma99[i] <= ma200[i]:
            crossings['bear'].append("bearish cross on *%s* %s at %s, price is %d" % (sym, tframe[5:], datetime.fromtimestamp(time[i]), df.close[i]))
            #print(crossings['bear'][-1], i)
            if i == length:
                return crossings['bear'][-1]

    #print(crossings)
    '''
    plt.plot(df.close, label=sym+' Price')
    plt.plot(ma50, label=sym+' 50 EMA')
    plt.plot(ma99, label=sym+' 99 EMA')
    plt.legend(loc='upper left')
    plt.show()
    '''
    return False
