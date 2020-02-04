# money_machine
crypto signal bot

be sure to use python 3

### runbot:
uses the code in mm.py to calculate signals, then will execute orders as appropriate. whenever an action is performed then a status message will be sent via telegram bot with status. 
default setting is:
- open orders with 3x leverage and 90% of available funds (configured in config.py)
- close the entire order at once
- only market orders
- only go long at beginning of uptrend, no short orders

To backtest the bot over the last 1000 days include 'test' in your command line options
To test without shorting add 'noshorts'. To test without longs add 'nolongs'.

### runday/runhour:
if you only want signals then these are used to calculate signals with selected coins and message the bot with results.

### mas_only:
returns crossing of moving averages

### mm:
returns trend changes (up or down or no change) as determined by currently selected moving average and smoothe factor. includes single EMA, triple EMA, hull MA,  and Tilson T3.
