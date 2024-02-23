# Author: Kyle W. McClintick <kyle.mcclintick@gmail.com>.

"""
Automatic trading toy

This script is comprised of the following sections:

    - Data feed: loads ticker data via Alpaca-py
    - Signal generation: trading opportunities are identified using some algorithm
    - Risk management: before making the trade, risk must be computed
    - Order execution: if risk and opportunity meet a criteria, the trade is executed
    - Post-Trade analysis: the outcome is analyzed to improve future trades

The module contains the following functions:

    - CLASSNAME -- description

References:
    [1] https://zodiactrading.medium.com/harnessing-the-power-of-high-frequency-trading-algorithms-in-python-a-comprehensive-guide-97ff0cd125c2
    [2] https://pypi.org/project/alpaca-trade-api/
"""

__version__ = '1.0'

import pandas
import logging.config
import torch
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame, TimeFrameUnit
import matplotlib.pyplot as plt

####################### USER DEFIND PARAMETERS #######################
key = ''  # get by creating an account at https://app.alpaca.markets/
secret = ''
base_url = 'https://paper-api.alpaca.markets'
symbol = 'VOO'  # ticker
time_resolution = 10  # Each data frame will be this far apart
time_unit = TimeFrameUnit.Minute  # units for the above
history_start = "2024-01-01"  # for VAR computation, how far back to look to
start_date = "2024-02-21"
end_date = "2024-02-21"
####################### USER DEFIND PARAMETERS #######################

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d]: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',  # Default is stderr
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
logging.config.dictConfig(LOGGING_CONFIG)
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Setting up data feed...')
logger.info(f'Accessing market via {base_url}')
logger.info(f'Using Alpaca API key: {key}, secret: {secret}')
api = tradeapi.REST(key, secret, base_url=base_url)

timeframe = TimeFrame(time_resolution, time_unit)
data = api.get_bars(symbol, timeframe, start_date, end_date).df
logger.debug(f'Raw data feed: \n{data}')
logger.info(f'Data frame columns: {data.keys()}')
logger.info(
    f'Retrieved {len(data)} frames of symbol {symbol} from {data.index.min()} to {data.index.max()}')

logger.info(f'Defining signal generation...')
data['Short_MA'] = data['close'].rolling(window=10).mean()
data['Long_MA'] = data['close'].rolling(window=50).mean()


def trade_logic(data):
    """
    Defines the signal generation
    :param data: feed, dtype: pandas data frame
    :return: Buy, Sell or Hold actions, dtype: string
    """
    assert type(data) is pandas.core.frame.DataFrame
    if data['Short_MA'][-1] > data['Long_MA'][-1]:
        return 'Buy'
    elif data['Short_MA'][-1] < data['Long_MA'][-1]:
        return 'Sell'
    else:
        return 'Hold'


logger.info(f'Estimating value at risk using historical method...')
history = api.get_bars(symbol, TimeFrame(1, TimeFrameUnit.Day), history_start, end_date).df
history["daily_return"] = history['close'].pct_change()
logger.debug(f'Daily returns since {history["daily_return"]}')
history['daily_return'].hist(bins=25)
plt.title(f'{symbol} Value at Risk, mean: {history["daily_return"].mean()}')
plt.xlabel('Daily change (%)')
plt.ylabel('Frequency')
plt.show()

logger.info(f'Executing trade...')
trade_signal = trade_logic(data)
if trade_signal == 'Buy' and history['daily_return'].mean() > 0:
    api.submit_order(
        symbol=symbol,
        qty=1,
        side='buy',
        type='market',
        time_in_force='gtc'
    )
    logger.info(f'Decision: buy order')
elif trade_signal == 'Sell':
    api.submit_order(
        symbol=symbol,
        qty=1,
        side='sell',
        type='market',
        time_in_force='gtc'
    )
    logger.info(f'Decision: sell order')
else:
    logger.info('Decision: hold order')

logger.info(f'Analyzing trade...')
plt.subplot(2, 1, 1)
data['close'].plot()
data['Short_MA'].plot()
data['Long_MA'].plot()
plt.legend()
plt.title(f'{symbol} data feed, decision: {trade_signal}')
plt.subplot(2, 1, 2)
history["daily_return"].plot()
plt.title('Daily returns')
plt.ylabel('% change')
plt.tight_layout()
plt.show()
