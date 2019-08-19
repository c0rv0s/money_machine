from mas_only import *
from mm import *
from utils import *

def runhour():
    print('runhour')
    data = fetch_data(1000, 'histohour', 'BTC')
    v = ma_job('BTC', 'histohour', data)
    if v:
        telegram_bot_sendtext(v)

    v = mm_job('BTC', 'histohour', data)
    if v:
        telegram_bot_sendtext(v)

    data = fetch_data(1000, 'histohour', 'XRP')
    v = ma_job('XRP', 'histohour', data)
    if v:
        telegram_bot_sendtext(v)
    
    v = mm_job('XRP', 'histohour', data)
    if v:
        telegram_bot_sendtext(v)

    data = fetch_data(1000, 'histohour', 'ETH')
    v = ma_job('ETH', 'histohour', data)
    if v:
        telegram_bot_sendtext(v)
    
    v = mm_job('ETH', 'histohour', data)
    if v:
        telegram_bot_sendtext(v)

runhour()
