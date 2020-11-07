from .models import Asset, AssetClass, Exchange


def update_asset_models(assets):
    """
    Update list of tradeable assets in database depending on what is available
    from Alpaca api.
    """
    # get list of unique exchanges
    exchanges = set(map(lambda asset: asset['exchange'], assets))
    asset_classes = set(map(lambda asset: asset['asset_class'], assets))

    # update exchanges
    for e in exchanges:
        exchange, _ = Exchange.objects.get_or_create(e)

    # update asset classes
    for a in asset_classes:
        asset_class, _ = AssetClass.objects.get_or_create(a)

    # from list of assets, create or update model instances
    for a in assets:
        asset, _ = Asset.objects.get_or_create(a)
