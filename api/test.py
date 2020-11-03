import logging
import os

import django
from django.conf import settings  # NOQA

os.environ['DJANGO_SETTINGS_MODULE'] = 'api.config.settings'
django.setup()

# Get an instance of a logger
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    import alpaca_trade_api as tradeapi

    # Env variables set to initalise connection:
    #   * APCA_API_KEY_ID
    #   * APCA_API_SECRET_KEY
    #   * APCA_API_BASE_URL
    api = tradeapi.REST()

    # Get our account information.
    account = api.get_account()

   # Check if our account is restricted from trading.
    if account.trading_blocked:
        logger.error('Account is currently restricted from trading.')

    # Check how much money we can use to open new positions.
    print('${} is available as buying power.'.format(account.buying_power))
