from mm import *
from utils import *

print('runbot')
data = fetch_data(1000, 'histoday', 'BTC')

signal = mm_job('BTC', 'histoday', data)
print(signal)
last_price = float( data[-1]['close'] )

#go long and send a message to telegram
if signal == 'up':
    o = open_order(last_price)
    if o == 0:
        telegram_bot_sendtext('XBT: bot going long')
    else:
        telegram_bot_sendtext('XBT: up trend begin, bot failed to open long')

#the other thing
if signal == 'down':
    o, bal = close_position()

    if o == 0:
        telegram_bot_sendtext('XBT: bot closing long, standing by for next entry, current balance is ' + str(bal))
    else:
        telegram_bot_sendtext('XBT: up trend over, bot failed to close position, current balance is ' + str(bal)')

