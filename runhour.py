from mas_only import *
from mm import *
from utils import *
import sys

def main():
    print('runhour')
    backtest = True if 'test' in sys.argv else False
    longs = True if 'nolongs' not in sys.argv else False 
    shorts = True if 'noshorts' not in sys.argv else False

    data = fetch_data(1000, 'histohour', 'BTC')
    signal = ma_job('BTC', 'histohour', data, backtest)
    if signal and not backtest:
        telegram_bot_sendtext(signal)

    signal = mm_job('BTC', 'histohour', data, backtest, shorts, longs)
    if signal and not backtest:
        telegram_bot_sendtext('BTC trend '+signal)

    data = fetch_data(1000, 'histohour', 'XRP')
    signal = ma_job('XRP', 'histohour', data, backtest)
    if signal and not backtest:
        telegram_bot_sendtext(signal)
    
    signal = mm_job('XRP', 'histohour', data, backtest, shorts, longs)
    if signal and not backtest:
        telegram_bot_sendtext('XRP trend '+signal)

    data = fetch_data(1000, 'histohour', 'ETH')
    signal = ma_job('ETH', 'histohour', data, backtest)
    if signal and not backtest:
        telegram_bot_sendtext(signal)
    
    signal = mm_job('ETH', 'histohour', data, backtest, shorts, longs)
    if signal and not backtest:
        telegram_bot_sendtext('ETH trend '+signal)

if __name__ == "__main__":
    main()
