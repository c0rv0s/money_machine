#!/usr/bin/env python3
from utils import *
import sys
import time
from mm import *
from config import *

def main():
    lastUpdate = 331301319
    messages = getUpdates(lastUpdate)
    if len(messages['result']) > 0:
        lastUpdate = messages['result'][-1]['update_id']
    while True:
        print('getting updates')
        try:
            messages = getUpdates(lastUpdate)
            for message in messages['result']:
                command = message['message']['text'].lower()
                chat_id = str(message['message']['chat']['id'])
                if command == 'balance' or command == 'wallet' or command =='bal':
                    data = fetch_data(1, 'histoday', 'BTC')
                    last_price = float( data[-1]['close'] )

                    bal = get_bal()
                    responseMessage = ""
                    if bal['position_value']:
                        responseMessage = """
Entry price: ${}
Open position value (BTC): {}
Unrealised Pnl (BTC): {}
Unrealised Pnl ($$): {}
Wallet Balance (BTC): {}
Wallet Balance ($$): {}
Current BTC Price: ${} 
                        """.format(bal['entry_price'], bal['position_value'], bal['unrealised_pnl'], last_price*float(bal['unrealised_pnl']), bal['wallet_balance'], last_price*float(bal['wallet_balance']), last_price)
                    else:
                        responseMessage = """
Wallet Balance (BTC): {}
Wallet Balance ($$): {}
Current BTC Price: ${} 
                        """.format(bal['wallet_balance'], last_price*float(bal['wallet_balance']), last_price)
                    telegram_bot_sendtext(responseMessage, chat_id)
                elif command == "close":
                    o = close_position()
                    bal = get_bal()['wallet_balance']

                    if o['ret_code'] == 0:
                        telegram_bot_sendtext('XBT: bot closing long, standing by for next entry, current balance is ' + str(bal), chat_id)
                    else:
                        telegram_bot_sendtext('XBT: bot failed to close position, current balance is ' + str(bal)+' error code: '+str(o['ret_code'])+' error msg: '+str(o['ret_msg']), chat_id)
                        log_error(o)
                elif command == 'history' or command == 'hist':
                    data = fetch_data(1000, 'histoday', ticker)
                    historical = mm_job(ticker, 'histoday', data, False, False, True, True)
                    telegram_bot_sendtext('\n'.join(historical),chat_id)
                else:
                    telegram_bot_sendtext("""
These are the commands I recognize:
History or Hist: displays results of analysis for last ten days
Balance or Bal: returns current balance and open positions
Close: emergency command to close currently open position
                    """, chat_id)
            if len(messages['result']) > 0:
                lastUpdate = messages['result'][-1]['update_id'] + 1
            time.sleep(1)
        except :
            telegram_bot_sendtext("Error with chat, resetting in 30 seconds...",chat_id)
            time.sleep(30)

if __name__ == '__main__':
    main()