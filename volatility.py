# script to calculate volatility on time series data

import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from datetime import datetime

from utils import *
from config import *

def average(data, period):
    index = [0]*period
    s = sum([abs(x) for x in data[:period]])
    for i in range(period, len(data)):
        s += abs(data[i])
        s -= abs(data[i-period])
        index.append(s/period)
    return index

def volatility(data, test):
    daily_changes = [100*(close - open)/open for close, open in zip(data['close'], data['open'])]
    std = np.std(daily_changes)
    stds = [c//std for c in daily_changes]
    vol_index = average(stds, 20)

    # for i, v in enumerate(vol_index):
    #     if v > 1.25:
    #         print(v, datetime.fromtimestamp(data['date'][i])) 

    # num_bins = 200
    # n, bins, patches = plt.hist(daily_changes, num_bins)
    # plt.xlabel('% change BTC price')
    # plt.ylabel('Number of days')
    # plt.show()

    # num_bins = 17
    # stdn, stdbins, stdpatches = plt.hist(stds, num_bins)
    # plt.xlabel('Stan dev of price change')
    # plt.ylabel('Number of days')
    # plt.show()
    # print([(x, standev) for x, standev in zip(stdn, stdbins)])

    # start = 0
    # for i in range(len(stds)):
    #     if stds[i] > 1 or stds[i] < -1:
    #         print(data['close'][start], data['close'][i], 'change:', data['close'][i] - data['close'][start])
    #         start = i

    t = [i for i in range(1001)]

    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('day')
    ax1.set_ylabel('price', color=color)
    ax1.plot(t, data['close'], color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('volitility', color=color)  # we already handled the x-label with ax1
    ax2.plot(t, vol_index, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()


if __name__ == "__main__":
    with open('8-14-eth.json') as json_file: 
        data = json.load(json_file) 

    volatility(data, True)


    # json = json.dumps(convert(fetch_data(1000, 'histoday', ticker)))
    # f = open("8-14-eth.json","w")
    # f.write(json)
    # f.close()