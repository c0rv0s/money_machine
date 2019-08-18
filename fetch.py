import requests

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
    api_uri = 'https://min-api.cryptocompare.com/data/'+time+'?fsym='+sym+'&tsym=USD&limit='+length+'&e=Kraken&api_key=fa05711eb31df6703c13a4672a8e84b65948dcb2f142a1f81b0c23b3dee57603'
    
    d = requests.get(api_uri).json()['Data']

    return d

