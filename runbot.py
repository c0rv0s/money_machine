from mm import *
from utils import *

print('runbot')
data = fetch_data(1000, 'histoday', 'BTC')

signal = mm_job('BTC', 'histoday', data)

last_price = float( data[-1]['close'] )

if signal == False:
    telegram_bot_sendtext('no change')

#go long and send a message to telegram
elif signal == 'up':
    telegram_bot_sendtext('XBT: new trend is up')
    o = open_order(last_price)
    if o['ret_code'] == 0:
        telegram_bot_sendtext('XBT: bot going long')
    else:
        telegram_bot_sendtext('XBT: bot failed to open long error report: ' + str(o))

#the other thing
elif signal == 'down':
    telegram_bot_sendtext('XBT: new trend is down')
    o = close_position()
    bal = get_bal()['wallet_balance']
    
    if o['ret_code'] == 0:
        telegram_bot_sendtext('XBT: bot closing long, standing by for next entry, current balance is ' + str(bal))
    else:
        telegram_bot_sendtext('XBT: up trend over, bot failed to close position, current balance is ' + str(bal)+' error report: '+str(o))
