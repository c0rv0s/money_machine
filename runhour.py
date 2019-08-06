from mas_only import job
def runhour():
    v = job('BTC', 'histohour')
    if v:
        telegram_bot_sendtext(v)
    v = job('XRP', 'histohour')
    if v:
        telegram_bot_sendtext(v)
    v = job('ETH', 'histohour')
    if v:
        telegram_bot_sendtext(v)

runhour()
