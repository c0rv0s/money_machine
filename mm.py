# script to calculate ultimate MA indicator and then report results to telegram

import math
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

from utils import convert
from config import *

def longLiq(entry, lev, maintMargenRate=0.005):
    return entry*lev / (lev+1 - (maintMargenRate*lev))
def shortLiq(entry, lev, maintMargenRate=0.005):
    return entry*lev / (lev-1 + (maintMargenRate*lev))

#full analysis method
def mm_job(sym, tframe, data, backtest, shorts=True, longs=True, history=False):
    len1 = 20
    a=0.7
    smoothe = 1 #1 to 10

    #get data
    length= len(data['date'])
    df = pd.DataFrame(data)
    df.columns = data.keys()

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
    #values for history
    historical = []
    for i in range(smoothe,length):
        change = False

        #liquidation calculator
        if trade and backtest:
            if direction == 'up':
                if data['close'][i] < longLiq(topen, leverage):
                    print("LONG LIQUIDATED")
            if direction == 'down':
                if data['close'][i] > shortLiq(topen, leverage):
                    print("SHORT LIQUIDATED")

        #direction change            
        if hullma[i] >= hullma[i - smoothe] and direction != 'up':
            direction = 'up'
            change = True

            if backtest:
                if i > 900:
                    print('new direction is up, '+str(datetime.fromtimestamp(data['date'][i]))+' $'+str(data['close'][i]))
                
                if trade and shorts:
                    amount = (balance * (topen / data['close'][i])) - balance
                    balance += (amount*leverage)*0.9974
                print('bought at '+str(data['close'][i])+' '+ str(datetime.fromtimestamp(data['date'][i]))+' new balance: '+str(balance))
                topen = data['close'][i]
                trade = True
                
        if hullma[i] < hullma[i - smoothe] and direction != 'down':
            direction = 'down'
            change = True
            
            if backtest:
                if i > 900:
                    print('new direction is down, '+str(datetime.fromtimestamp(data['date'][i]))+' $'+str(data['close'][i]))
                
                if trade and longs:
                    amount = (balance * (data['close'][i])/topen) - balance
                    balance += (amount*leverage)*0.9974
                print('sold at '+str(data['close'][i])+' '+ str(datetime.fromtimestamp(data['date'][i]))+' new balance: '+str(balance))
                topen = data['close'][i]
                trade = True
            
        if backtest:
            vals.append(balance)
            if i > 990:
                print("close, hullma", data['close'][i], hullma[i])
        if history and i > 990:
            historical.append('Price: '+str(data['close'][i])+' '+ 'MA: ' + str(hullma[i]) + ' Direction: ' + direction)
            
    if backtest:        
        plt.plot(vals)
        plt.show()
    if history:
        return historical
    if change:
        return direction
    else:
        return False
