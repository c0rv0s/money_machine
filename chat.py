#!/usr/bin/env python3
from utils import *
import sys
import time

def main():
    lastUpdate = 331301319
    messages = getUpdates(lastUpdate)
    if len(messages['result']) > 0:
        lastUpdate = messages['result'][-1]['update_id'] + 1
    while True:
        try:
            messages = getUpdates(lastUpdate)
            for message in messages['result']:
                command = message['message']['text'].lower()
                chat_id = str(message['message']['chat']['id'])
                if command == 'balance' or command == 'wallet':
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
                else:
                    telegram_bot_sendtext("""
These are the commands I recognize:
Wallet or Balance: returns current balance and open positions
Close: emergency command to close currently open position
                    """, chat_id)
            if len(messages['result']) > 0:
                lastUpdate = messages['result'][-1]['update_id'] + 1
            time.sleep(6)
        except :
            telegram_bot_sendtext("Error with chat",chat_id)
            break

if __name__ == '__main__':
    main()