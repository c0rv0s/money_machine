from utils import *
import sys
import time

def main():
    lastUpdate = 331301188
    while True:
        messages = getUpdates(lastUpdate)
        for message in messages['result']:
            command = message['message']['text'].lower()
            chat_id = str(message['message']['chat']['id'])
            print(message)
            if command == 'balance' or command == 'wallet':
                bal = get_bal()
                print(bal)
                telegram_bot_sendtext('cow', chat_id)
        lastUpdate = messages['result'][-1]['update_id'] + 1
        time.sleep(30)

if __name__ == '__main__':
    main()