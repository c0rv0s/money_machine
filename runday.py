from mas_only import *
from mm import *
from utils import *

def runday():
    print('runday')
    data = fetch_data(1000, 'histoday', 'BTC')
    signal = ma_job('BTC', 'histoday', data)
    if signal:
        telegram_bot_sendtext(signal)
    
    signal = mm_job('BTC', 'histoday', data)
    if signal:
        telegram_bot_sendtext('BTC trend '+signal)
    
    data = fetch_data(1000, 'histoday', 'XRP')
    signal = ma_job('XRP', 'histoday', data)
    if signal:
        telegram_bot_sendtext(signal)
    
    signal = mm_job('XRP', 'histoday', data)
    if signal:
        telegram_bot_sendtext('XRP trend '+signal)
    
    data = fetch_data(1000, 'histoday', 'ETH')
    signal = ma_job('ETH', 'histoday', data)
    if signal:
        telegram_bot_sendtext(signal)
    
    signal = mm_job('ETH', 'histoday', data)
    if signal:
        telegram_bot_sendtext('ETH trend '+signal)

runday()
