import json
import logging

from server.config import celery_app
from server.core.utils import TradeApiRest
from django.forms.models import model_to_dict

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

    # Get unique entries
    assets = list(map(lambda asset: asset.__dict__['_raw'], assets))
    exchanges = set(map(lambda asset: asset['exchange'], assets))
    asset_classes = set(map(lambda asset: asset['class'], assets))

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
    # for item in assets[1:10]:
    #     # Rename 'asset' to 'asset_class' to match model schema
    #     item['asset_class'] = AssetClass.objects.get(name=item['class'])
    #     item['exchange'] = Exchange.objects.get(name=item['exchange'])
    #     del item['class']

    #     # TO DO -> CREATE BULK ADD SERIALIZER

    #     _, created = Asset.objects.get_or_create(**item)
    #     if created:
    #         additions_to_db += 1

    # serializer = AssetBulkCreateSerializer(data=assets, many=True)

    # serializer.is_valid(raise_exception=True)
    # serializer.save()

    logger.info(f"Updates to asset models: {additions_to_db}")


@celery_app.task(ignore_result=True)
def bulk_add_assets(assets):
    """
    Bulk create assets.

    :param assets(list): list of serialized assets to be created
    """
    return Asset.objects.bulk_create(
        objs=assets, batch_size=500, ignore_conflicts=True
    )
