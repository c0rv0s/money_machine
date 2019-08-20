import requests
import hashlib
import hmac
import base64
import time
from tokens import *

def telegram_bot_sendtext(bot_message):
    
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + chat_id + '&parse_mode=Markdown&text=' + bot_message
    
    response = requests.get(send_text)
    
    return response.json()

def convert(d):
    volume = []
    close = []
    open = []
    time = []
    for entry in d:
        volume.append(entry['volumeto'])
        close.append(entry['close'])
        open.append(entry['open'])
        time.append(entry['time'])
    return volume, close, open, time

#request data from crypto compare
# t= histohour
# t = histoday
def fetch_data(length, time, sym):
    length = str(length)
    api_uri = 'https://min-api.cryptocompare.com/data/'+time+'?fsym='+sym+'&tsym=USD&limit='+length+'&e=Bitstamp&api_key='+key
    
    d = requests.get(api_uri).json()['Data']

    return d

#bybit stuff
def timestamp():
    return int(round(time.time() * 1000))

def get_bal():
    url = 'https://api.bybit.com/position/list'
    param_str = 'api_key=' + api_key + '&timestamp=' + str(timestamp())
    
    message = bytes(param_str, 'utf-8')
    secret = bytes(private_key, 'utf-8')

    sign = hmac.new(secret, message, digestmod=hashlib.sha256).digest().hex()
    
    p = url + '?' + param_str + '&sign=' + sign
    print(p)
    response = requests.get(p).json()
    print(response)

def open_order():
    url = 'https://api.bybit.com/open-api/order/create'
    side = 'side=Buy'
    symbol = 'symbol=BTCUSD'
    order_type = 'order_type=Market'


