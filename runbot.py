from mm import *
from utils import *
from config import *
import sys

def main():
    print('runbot')
    data = convert(fetch_data(1000, 'histoday', ticker))

    backtest = True if 'test' in sys.argv else False
    longs = True if 'nolongs' not in sys.argv else False 
    shorts = True if 'noshorts' not in sys.argv else False

    signal = mm_job(ticker, 'histoday', data, backtest, shorts, longs)
    print('Signal: ' + str(signal))

    last_price = float( data['close'][-1] )
    print('last price: $'+str(last_price))

    if not backtest:
        if signal == False:
            telegram_bot_sendtext('no change, '+ticker+' last price: $' + str(last_price))

        #go long and send a message to telegram
        elif signal == 'up':
            telegram_bot_sendtext(ticker + ': new trend is up, last price: $' + str(last_price))
            o = open_order(last_price)
            if o['ret_code'] == 0:
                telegram_bot_sendtext(ticker + ': bot going long')
            else:
                telegram_bot_sendtext(ticker + ': bot failed to open long, error code: '+str(o['ret_code'])+' error msg: '+str(o['ret_msg']))
                log_error(o)

        #the other thing
        elif signal == 'down':
            telegram_bot_sendtext(ticker + ': new trend is down, last price: $' + str(last_price))
            o = close_position()
            bal = get_bal()['wallet_balance']

            if o['ret_code'] == 0:
                telegram_bot_sendtext(ticker + ': bot closing long, standing by for next entry, current balance is ' + str(bal))
            else:
                telegram_bot_sendtext(ticker + ': bot failed to close position, current balance is ' + str(bal)+' error code: '+str(o['ret_code'])+' error msg: '+str(o['ret_msg']))
                log_error(o)


if __name__ == "__main__":
    main()