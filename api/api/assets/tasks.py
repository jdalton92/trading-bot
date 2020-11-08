import logging

from api.config import celery_app
from api.core.utils import TradeApiRest

from .models import Asset, AssetClass, Exchange

logger = logging.getLogger(__name__)


@celery_app.task(ignore_result=True)
def update_asset_models():
    """
    Update list of tradeable assets in database depending on what is available
    from Alpaca api.
    """
    logger.info('Updating asset, asset class, and exchange models...')

    api = TradeApiRest()
    assets = api._list_assets()

    # Get list of unique exchanges
    exchanges = set(map(lambda asset: asset['exchange'], assets))
    asset_classes = set(map(lambda asset: asset['asset_class'], assets))

    # Set up total count of additions to database
    additions_to_db = 0

    # Update exchanges
    for item in exchanges:
        exchange, created = Exchange.objects.update_or_create(
            name=item,
            defaults={'is_current': 'True'}
        )
        if created:
            additions_to_db += 1

    # Update asset classes
    for item in asset_classes:
        asset_class, created = AssetClass.objects.update_or_create(
            name=item,
            defaults={'is_current': 'True'}
        )
        if created:
            additions_to_db += 1

    # From list of assets, create or update model instances
    for a in assets:
        asset, created = Asset.objects.update_or_create(
            **a,
            defaults={'is_current': 'True'}
        )
        if created:
            additions_to_db += 1

    logger.info(f"Updates: {additions_to_db}")

    # CHECK IF EXISTS IN DB BUT NOT IN NEW LIST, AND SET IS_CURRENT TO FALSE
