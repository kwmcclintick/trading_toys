# trading_toys.py
> "High-frequency trading (HFT) has evolved to become an integral part of the modern financial landscape. Often viewed with a sense of mystique and awe, HFT involves the execution of complicated financial strategies by advanced algorithms.
> These algorithms process enormous amounts of data in real time to make trading decisions within fractions of a second. The aim is simple: to capitalize on minuscule price differences or trends that appear for only a short period of time. In this article, we’ll delve into how HFT algorithms function in fundamental financial markets and how you can build your own HFT algorithm using Python as an example." - Harnessing the Power of High-Frequency Trading Algorithms in Python: A Comprehensive Guide

This script is comprised of the following sections:

    - Data feed: loads ticker data via Alpaca-py
    - Signal generation: trading opportunities are identified using some algorithm
    - Risk management: before making the trade, risk must be computed
    - Order execution: if risk and opportunity meet a criteria, the trade is executed
    - Post-Trade analysis: the outcome is analyzed to improve future trades

# dash boards
[FRED dashboard: Real estate](https://fredaccount.stlouisfed.org/dashboard/108849#)

[FRED dashboard: Food](https://fredaccount.stlouisfed.org/dashboard/108852#)
