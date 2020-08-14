from mas_only import *
from mm import *
from utils import *
import sys

def main():
    backtest = True if 'test' in sys.argv else False
    longs = True if 'nolongs' not in sys.argv else False 
    shorts = True if 'noshorts' not in sys.argv else False
    timeframe = ''
    if 'hour' in sys.argv: timeframe = 'hour'
    elif 'day' in sys.argv: timeframe = 'day'
    else: 
        timeframe = 'day'
        print('No suitable timeframe provided, using day by default')
    tickers = []
    if 'btc' in sys.argv or 'BTC' in sys.argv: tickers.append('BTC')
    if 'eth' in sys.argv or 'ETH' in sys.argv: tickers.append('ETH')
    if 'xrp' in sys.argv or 'XRP' in sys.argv: tickers.append('XRP')
    if not tickers:
        tickers.append('BTC')
        print('No tickers provided, using BTC by default')

    for ticker in tickers:
        data = convert(fetch_data(1000, 'histo'+timeframe, ticker))
        signal = ma_job(ticker, 'histo'+timeframe, data, backtest)
        if signal and not backtest:
            telegram_bot_sendtext(signal)

if __name__ == "__main__":
    main()
