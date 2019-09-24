from mm import *
from utils import *

print('runbot')
data = fetch_data(1000, 'histoday', 'BTC')

signal = mm_job('BTC', 'histoday', data)
print('Signal: ' + str(signal))

last_price = float( data[-1]['close'] )
print('last price: $'+str(last_price))

if signal == False:
    telegram_bot_sendtext('no change, last price: $' + str(last_price))

#go long and send a message to telegram
elif signal == 'up':
    telegram_bot_sendtext('XBT: new trend is up, last price: $' + str(last_price))
    o = open_order(last_price)
    if o['ret_code'] == 0:
        telegram_bot_sendtext('XBT: bot going long')
    else:
        telegram_bot_sendtext('XBT: bot failed to open long, error code: '+str(o['ret_code'])+' error msg: '+str(o['ret_msg']))

#the other thing
elif signal == 'down':
    telegram_bot_sendtext('XBT: new trend is down, last price: $' + str(last_price))
    o = close_position()
    bal = get_bal()['wallet_balance']
    
    if o['ret_code'] == 0:
        telegram_bot_sendtext('XBT: bot closing long, standing by for next entry, current balance is ' + str(bal))
    else:
        telegram_bot_sendtext('XBT: bot failed to close position, current balance is ' + str(bal)+' error code: '+str(o['ret_code'])+' error msg: '+str(o['ret_msg']))

