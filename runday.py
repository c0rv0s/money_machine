from mas_only import *
from mm import *
from utils import *

def main():
    print('runday')
    backtest = True if 'test' in sys.argv else False
    longs = True if 'nolongs' not in sys.argv else False 
    shorts = True if 'noshorts' not in sys.argv else False

    data = fetch_data(1000, 'histoday', 'BTC')
    signal = ma_job('BTC', 'histoday', data)
    if signal and not backtest:
        telegram_bot_sendtext(signal)
    
    signal = mm_job('BTC', 'histoday', data, backtest, shorts, longs)
    if signal and not backtest:
        telegram_bot_sendtext('BTC trend '+signal)
    
    data = fetch_data(1000, 'histoday', 'XRP')
    signal = ma_job('XRP', 'histoday', data)
    if signal and not backtest:
        telegram_bot_sendtext(signal)
    
    signal = mm_job('XRP', 'histoday', data, backtest, shorts, longs)
    if signal and not backtest:
        telegram_bot_sendtext('XRP trend '+signal)
    
    data = fetch_data(1000, 'histoday', 'ETH')
    signal = ma_job('ETH', 'histoday', data)
    if signal and not backtest:
        telegram_bot_sendtext(signal)
    
    signal = mm_job('ETH', 'histoday', data, backtest, shorts, longs)
    if signal and not backtest:
        telegram_bot_sendtext('ETH trend '+signal)

if __name__ == "__main__":
    main()
