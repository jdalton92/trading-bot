import logging

from server.config import celery_app
from server.core.utils import TradeApiRest

from .models import Asset, AssetClass, Exchange
from .serializers import AssetSerializer

logger = logging.getLogger(__name__)


def update_asset_models():
    """
    Update list of tradeable assets in database depending on what is available
    from Alpaca api.
    """
    api = TradeApiRest()
    assets = api._list_assets()
    update_asset_models(assets)


def update_asset_models(assets):
    """
    Update assets, asset classes, and exchange models from list of assets

    :param assets(list): list of assets
    """
    logger.info('Updating asset, asset class, and exchange models...')

    # Transform Alpaca response into asset model format
    assets = list(map(lambda asset: asset.__dict__['_raw'], assets))
    exchanges = set(map(lambda asset: asset['exchange'], assets))
    asset_classes = set(map(lambda asset: asset['class'], assets))

    additions_to_db = 0

    for item in exchanges:
        _, created = Exchange.objects.get_or_create(name=item)
        if created:
            additions_to_db += 1

    for item in asset_classes:
        _, created = AssetClass.objects.get_or_create(name=item)
        if created:
            additions_to_db += 1

    existing_assets = [
        str(asset) for asset in Asset.objects.all().values_list('id', flat=True)
    ]
    new_assets = [
        asset for asset in assets if asset['id'] not in existing_assets
    ]
    bulk_add_assets(new_assets)

    additions_to_db += len(new_assets)

    logger.info(f"Updates to asset models: {additions_to_db}")


@celery_app.task(ignore_result=True)
def bulk_add_assets(assets):
    """
    Bulk create assets.

    :param assets(list): list of serialized assets to be created
    """
    for asset in assets:
        asset['asset_class'] = asset['class']
        del asset['class']
        serializer = AssetSerializer(data=asset)
        if serializer.is_valid():  # Fail silently for bulk add
            serializer.save()
