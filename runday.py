from mas_only import *
from mm import *
from send import telegram_bot_sendtext
from fetch import fetch_data

def runday():
    print('runday')
    data = fetch_data(1000, 'histoday', 'BTC')
    v = ma_job('BTC', 'histoday', data)
    if v:
        telegram_bot_sendtext(v)
    
    v = mm_job('BTC', 'histoday', data)
    if v:
        telegram_bot_sendtext(v)
    
    data = fetch_data(1000, 'histoday', 'XRP')
    v = ma_job('XRP', 'histoday', data)
    if v:
        telegram_bot_sendtext(v)
    
    v = mm_job('XRP', 'histoday', data)
    if v:
        telegram_bot_sendtext(v)
    
    data = fetch_data(1000, 'histoday', 'ETH')
    v = ma_job('ETH', 'histoday', data)
    if v:
        telegram_bot_sendtext(v)
    
    v = mm_job('ETH', 'histoday', data)
    if v:
        telegram_bot_sendtext(v)

runday()
