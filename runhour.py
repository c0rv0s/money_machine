from mas_only import *
from mm import *
from utils import *

def runhour():
    print('runhour')
    data = fetch_data(1000, 'histohour', 'BTC')
    signal = ma_job('BTC', 'histohour', data)
    if signal:
        telegram_bot_sendtext(signal)

    signal = mm_job('BTC', 'histohour', data)
    if signal:
        telegram_bot_sendtext('BTC trend '+signal)

    data = fetch_data(1000, 'histohour', 'XRP')
    signal = ma_job('XRP', 'histohour', data)
    if signal:
        telegram_bot_sendtext(signal)
    
    signal = mm_job('XRP', 'histohour', data)
    if signal:
        telegram_bot_sendtext('XRP trend '+signal)

    data = fetch_data(1000, 'histohour', 'ETH')
    signal = ma_job('ETH', 'histohour', data)
    if signal:
        telegram_bot_sendtext(signal)
    
    signal = mm_job('ETH', 'histohour', data)
    if signal:
        telegram_bot_sendtext('ETH trend '+signal)

runhour()
