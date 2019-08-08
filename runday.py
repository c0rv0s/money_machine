from mas_only import *
from mm import *

def runday():
    #simple
    v = job('BTC', 'histoday')
    if v:
        telegram_bot_sendtext(v)
    v = job('XRP', 'histoday')
    if v:
        telegram_bot_sendtext(v)
    v = job('ETH', 'histoday')
    if v:
        telegram_bot_sendtext(v)
    #ultimate
    v = mm_job('BTC', 'histoday')
    if v:
        mm_telegram_bot_sendtext(v)
    v = mm_job('XRP', 'histoday')
    if v:
        mm_telegram_bot_sendtext(v)
    v = mm_job('ETH', 'histoday')
    if v:
        mm_telegram_bot_sendtext(v)

runday()
