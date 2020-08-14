# money_machine
crypto signal bot

Be sure to use python 3

### runbot:
uses the code in mm.py to calculate signals, then will execute orders as appropriate. whenever an action is performed then a status message will be sent via telegram bot with status. 

Default setting is:
- open orders with 3x leverage and 90% of available funds (configured in config.py)
- close the entire order at once
- only market orders
- only go long at beginning of uptrend, no short orders

To backtest the bot over the last 1000 days include 'test' in your command line options
To test without shorting add 'noshorts'. To test without longs add 'nolongs'.

### runmabot:
If you only want signals then these are used to calculate signals with selected coins and message the bot with results.
```test```, ```noshorts``` and ```nolongs``` can be used as options here for testing.
```hour``` or ```day``` can be passed to specifiy timeframe and ```btc```, ```eth``` and ```xrp``` will be accepted as ticker arguments. 

### mas_only:
Returns crossing of moving averages

### mm:
Returns trend changes (up or down or no change) as determined by Hull Moving Average and smoothe factor.

## chat:
On linux run ```nohup python3 \path\to\chat.py &``` to run the chat server in the background for balance queries on demand
