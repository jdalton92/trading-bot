import logging

from alpaca_trade_api.entity import Asset as AlpacaAsset
from server.config import celery_app
from server.core.alpaca import TradeApiRest

from .models import Asset, AssetClass, Exchange
from .serializers import AssetSerializer, BarSerializer

logger = logging.getLogger(__name__)


def update_assets(assets=None):
    """
    Update list of tradeable assets in database depending on what is available
    from Alpaca api.

    :param assets(list): list of assets
    """
    logger.info("Updating asset, asset class, and exchange models...")

    if not assets:
        api = TradeApiRest()
        assets = api._list_assets()

    # Transform Alpaca response into dict required by Asset model
    if isinstance(assets[0], AlpacaAsset):
        assets = list(map(lambda asset: asset.__dict__["_raw"], assets))
        exchanges = set(map(lambda asset: asset["exchange"], assets))
        asset_classes = set(map(lambda asset: asset["class"], assets))
    else:
        exchanges = set(map(lambda asset: asset["exchange"], assets))
        asset_classes = set(map(lambda asset: asset["class"], assets))

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
        str(asset_id) for asset_id in Asset.objects.all().values_list("id", flat=True)
    ]
    new_assets = [asset for asset in assets if asset["id"] not in existing_assets]
    bulk_add_assets(new_assets)

    additions_to_db += len(new_assets)

    logger.info(f"Updates to asset models: {additions_to_db}")


@celery_app.task(ignore_result=True)
def bulk_add_assets(assets):
    """
    Bulk create assets.

    :param assets(list): list of assets to be created
    """
    for asset in assets:
        if asset.get("class"):
            asset["asset_class"] = asset["class"]
            del asset["class"]
        serializer = AssetSerializer(data=asset)
        # Fail silently for bulk add
        if serializer.is_valid():
            serializer.save()


@celery_app.task(ignore_result=True)
def get_quotes(symbols):
    """Fetch latest quote for list of symbols."""
    if not isinstance(symbols, list):
        symbols = [symbols]
    api = TradeApiRest()
    quotes = {}
    errors = 0
    for symbol in symbols:
        try:
            quotes[symbol] = api._get_last_quote(symbol)
        except Exception:
            errors += 1
    if errors:
        logger.error(f"Errors fetching stock quotes: {errors}")
    return quotes


@celery_app.task(ignore_result=True)
def update_bars(
    symbols, timeframe, limit=None, start=None, end=None, after=None, until=None
):
    """Fetch bar data for list of symbols."""
    if not isinstance(symbols, list):
        symbols = [symbols]
    api = TradeApiRest()
    try:
        assets_bars = api._get_bars(symbols, timeframe, limit, start, end, after, until)
    except Exception as e:
        logger.error(f"Errors fetching bars: {e}")

    for asset_symbol in assets_bars:
        for bar in assets_bars[asset_symbol]:
            bar = bar.__dict__["_raw"]
            bar["asset"] = asset_symbol
            serializer = BarSerializer(data=bar)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

    return assets_bars
