import json
import logging

from api.config import celery_app
from api.core.utils import TradeApiRest
from django.forms.models import model_to_dict

from .models import Asset, AssetClass, Exchange
from .serializers import AssetSerializer

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
    exchanges = set(map(
        lambda asset: asset.__dict__['_raw']['exchange'],
        assets
    ))
    asset_classes = set(map(
        lambda asset: asset.__dict__['_raw']['class'],
        assets
    ))

    # Set up total count of additions to database
    additions_to_db = 0

    # Update exchanges
    for item in exchanges:
        _, created = Exchange.objects.get_or_create(name=item)
        if created:
            additions_to_db += 1

    # Update asset classes
    for item in asset_classes:
        _, created = AssetClass.objects.get_or_create(name=item)
        if created:
            additions_to_db += 1

    # From list of assets, create or update model instances
    for item in assets:
        _, created = Asset.objects.get_or_create(**item)
        if created:
            additions_to_db += 1

    logger.info(f"Updates: {additions_to_db}")
