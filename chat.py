#!/usr/bin/env python3
from utils import *
import time
import _thread
from mm import *
from config import *

def gasBot():
    while True:
        try:
            gas = get_gas()
            standard = gas['standard'] // 1e9
            fast = gas['fast'] // 1e9
            if standard <= 30:
                msg = '''
Gas is cheap right now!
Fast: {}
Standard: {}
                '''.format(fast, standard)
                telegram_bot_sendtext(msg)
            time.sleep(60)
        except:
            telegram_bot_sendtext("Error with gasBot", chat_id)
            break

def chatBot():
    lastUpdate = 331301684
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
PnL: {}%
Current BTC Price: ${} 
                        """.format(bal['entry_price'], bal['position_value'], bal['unrealised_pnl'], last_price*float(bal['unrealised_pnl']), bal['wallet_balance'], last_price*float(bal['wallet_balance']), truncate(100*bal['unrealised_pnl']/bal['wallet_balance'], 4), last_price)
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
                elif command == "long":
                    bal = get_bal()
                    if bal['position_value']:
                        telegram_bot_sendtext('You already have an open position. Please close before opening a new one.', chat_id)
                    else:
                        o = open_order(last_price)
                        if o['ret_code'] == 0:
                            telegram_bot_sendtext(ticker + ': bot going long', chat_id)
                        else:
                            telegram_bot_sendtext(ticker + ': bot failed to open long, error code: '+str(o['ret_code'])+' error msg: '+str(o['ret_msg']), chat_id)
                            log_error(o)
                elif command == "short":
                    bal = get_bal()
                    if bal['position_value']:
                        telegram_bot_sendtext('You already have an open position. Please close before opening a new one.', chat_id)
                    else:
                        o = open_order(last_price, side='Sell')
                        if o['ret_code'] == 0:
                            telegram_bot_sendtext(ticker + ': bot going short', chat_id)
                        else:
                            telegram_bot_sendtext(ticker + ': bot failed to open short, error code: '+str(o['ret_code'])+' error msg: '+str(o['ret_msg']), chat_id)
                            log_error(o)
                elif command == 'history' or command == 'hist':
                    data = convert(fetch_data(1000, 'histoday', ticker))
                    historical = mm_job(ticker, 'histoday', data, False, False, True, True)
                    telegram_bot_sendtext('\n'.join(historical), chat_id)
                elif command == 'stock' or command == 's2f':
                    telegram_bot_sendtext("This feature is still in development, most likely permanently", chat_id)
                elif command == 'gas':
                    gas = get_gas()
                    standard = gas['standard'] // 1e9
                    fast = gas['fast'] // 1e9
                    telegram_bot_sendtext("Fast: " + str(fast) + ", Standard: " + str(standard), chat_id)
                else:
                    telegram_bot_sendtext("""
These are the commands I recognize:
History or Hist: displays results of analysis for last ten days
Balance or Bal: returns current balance and open positions
Close: emergency command to close currently open position
Stock or s2f: shows an analysis of where bitcoin currently is on the Stock to Flow model
Long: opens a long if there is no currently open position
Short: opens a short if there is no currently open position
Gas: current Ethereum gas prices
                    """, chat_id)
            if len(messages['result']) > 0:
                lastUpdate = messages['result'][-1]['update_id'] + 1
            time.sleep(3)
        except:
            telegram_bot_sendtext("Error with chatBot", chat_id)
            break


try:
    _thread.start_new_thread( gasBot, () )
    _thread.start_new_thread( chatBot, () )
except:
    print ("Error: unable to start thread")

while 1:
   pass

