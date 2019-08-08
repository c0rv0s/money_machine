from mas_only import *
from mm import *

def runhour():
    #simple
    v = job('BTC', 'histohour')
    if v:
        telegram_bot_sendtext(v)
    v = job('XRP', 'histohour')
    if v:
        telegram_bot_sendtext(v)
    v = job('ETH', 'histohour')
    if v:
        telegram_bot_sendtext(v)
    #ultimate
    v = mm_job('BTC', 'histohour')
    if v:
        mm_telegram_bot_sendtext(v)
    v = mm_job('XRP', 'histohour')
    if v:
        mm_telegram_bot_sendtext(v)
    v = mm_job('ETH', 'histohour')
    if v:
        mm_telegram_bot_sendtext(v)

runhour()
