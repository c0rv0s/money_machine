
from mas_only import job
def runday():
    v = job('BTC', 'histoday')
    if v:
        telegram_bot_sendtext(v)
    v = job('XRP', 'histoday')
    if v:
        telegram_bot_sendtext(v)
    v = job('ETH', 'histoday')
    if v:
        telegram_bot_sendtext(v)

runday()
