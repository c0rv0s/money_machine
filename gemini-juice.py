# script to calculate ultimate MA indicator and then report results to telegram

import requests, math, time

chat_id =  '-1001333491977'

#reading text files doesn't work on Heroku >:(
'''
    signals = {'BTC':0,'ETH':0}
    
    def read_signals():
    global signals
    with open("signals.txt") as f:
    mylist = f.read().splitlines()
    signals['BTC'] = float(mylist[0])
    signals['ETH'] = float(mylist[1])
    open("signals.txt","w").close()
    
    def write_signals():
    global signals
    file = open("signals.txt", "w")
    file.write(str(signals['BTC']))
    file.write('\n')
    file.write(str(signals['ETH']))
    file.close()
    '''

#run BTC bot function begin
def run_bot(ticker, pair, period, exchange):
    data = 'https://min-api.cryptocompare.com/data/histohour?fsym='+str(ticker)+'&tsym='+str(pair)+'&limit='+str(period)+'&e='+str(exchange)
    price = 'https://min-api.cryptocompare.com/data/price?fsym='+str(ticker)+'&tsyms='+str(pair)+'&e='+str(exchange)
    bot_update = 'https://api.telegram.org/bot543273158:AAF2oIv8s4kE6NJ9NoTK08UbQJKcqpqxUjA/sendMessage'
    
    d = requests.get(data).json()
    p = requests.get(price).json()
    
    #if there's an error alert
    if d['Response'] != 'Success':
        print(d['Response'])
        error_msg = "ERROR("+str(ticker)+"): " + str(['Response'])
        t = requests.post(bot_update, {'chat_id': chat_id,'text': error_msg})
    #everything is good, go on
    else:
        gain = 0
        loss = 0
        x = 1
        avgGain = 0
        avgLoss = 0
        current_RSI = 0
        highest_RSI = 0
        lowest_RSI = 0
        for candle in d['Data']:
            if x <= 14:
                if ( candle['close'] > candle['open'] ):
                    gain += ( candle['close'] - candle['open'] )
                else:
                    loss += ( candle['open'] - candle['close'] )
            if x == 14:
                avgGain = gain / 14
                avgLoss = loss / 14
            if x > 14:
                if ( candle['close'] > candle['open'] ):
                    avgGain = ( (avgGain * 13) + ( candle['close'] - candle['open'] ) ) / 14
                else:
                    avgLoss = ( (avgLoss * 13) + ( candle['open'] - candle['close'] ) ) / 14
                
                current_RSI = 100 - ( 100 / ( 1 + (avgGain / avgLoss) ) )
                if current_RSI > highest_RSI:
                    highest_RSI = current_RSI
                if current_RSI < lowest_RSI:
                    lowest_RSI = current_RSI

        x += 1

#calculate stoch and round rsi
stoch_RSI = math.floor( 100 * (current_RSI - lowest_RSI) / (highest_RSI - lowest_RSI) )
current_RSI = math.floor( current_RSI )
#print info to console
rsi_string = str(ticker)+" RSI is: " + str(current_RSI )
    stoch_string = str(ticker)+" Stoch RSI is: " + str(stoch_RSI)
    if pair == 'USD':
        price_string = "Current " + str(ticker) + " price is $" + str(p[pair])
        else:
            price_string = "Current " + str(ticker) + " price is B" + str(p[pair])

    print(rsi_string)
        print(stoch_string)
        print(price_string)
        
        #send to telegram if buy or sell signal active
        full_msg = rsi_string + '\n' + stoch_string + '\n' + price_string + '\n'
        
        if stoch_RSI >= 80 and current_RSI >= 70:
            t = requests.post(bot_update, {'chat_id': chat_id,
                              'text': full_msg + '*SUGGESTED: STRONG SELL*',
                              'parse_mode': 'Markdown'})

        if (stoch_RSI >= 80 and current_RSI < 70) or (stoch_RSI < 80 and current_RSI >= 70):
            t = requests.post(bot_update, {'chat_id': chat_id,
                              'text': full_msg + '*SUGGESTED: SELL*',
                              'parse_mode': 'Markdown'})

if stoch_RSI <= 20 and current_RSI <= 30:
    t = requests.post(bot_update, {'chat_id': chat_id,
                      'text': full_msg + '*SUGGESTED: STRONG BUY*',
                      'parse_mode': 'Markdown'})
        if (stoch_RSI <= 20 and current_RSI > 30) or (stoch_RSI > 20 and current_RSI <= 30):
            t = requests.post(bot_update, {'chat_id': chat_id,
                              'text': full_msg + '*SUGGESTED: BUY*',
                              'parse_mode': 'Markdown'})


#end run bot function

#main
#read_signals()
run_bot('BTC', 'USD', 4800, 'Gemini')
run_bot('ETH', 'USD', 4800, 'Gemini')
run_bot('ADA', 'BTC', 800, 'Binance')
#write_signals()



#end
