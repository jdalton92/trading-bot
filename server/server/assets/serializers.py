from rest_framework import serializers

from .models import Asset, AssetClass, Bar, Exchange


class AssetSerializer(serializers.ModelSerializer):
    """Serializer for tradeable assets via Alpaca api."""

    id = serializers.UUIDField(format='hex_verbose')
    asset_class = serializers.SlugRelatedField(
        queryset=AssetClass.objects.all(),
        slug_field="name",
        required=True
    )
    exchange = serializers.SlugRelatedField(
        queryset=Exchange.objects.all(),
        slug_field="name",
        required=True
    )

    class Meta:
        model = Asset
        fields = '__all__'


class AssetClassSerializer(serializers.ModelSerializer):
    """
    Serializer for asset classes available for tradeable assets via Alpaca api.
    """

    class Meta:
        model = AssetClass
        fields = '__all__'


class ExchangeSerializer(serializers.ModelSerializer):
    """
    Serializer for exchanges available for tradeable assets via Alpaca api.
    """

    class Meta:
        model = Exchange
        fields = '__all__'


class BarSerializer(serializers.ModelSerializer):
    """
    Serializer for bar data for tradeable assets via Alpaca api.
    """

    asset = serializers.SlugRelatedField(
        queryset=Asset.objects.all(),
        slug_field="symbol",
        required=True
    )

    class Meta:
        model = Bar
        fields = '__all__'

    def validate(self, data):
        """Validate bar data."""
        print('\n\nself.kwargs', self.kwargs)
        request_asset_id = self.context['asset_id']
        # When updating bar, the data might not have the asset field
        bar_asset_id = (
            data['asset'].id if data.get('asset') else self.instance.asset.pk
        )

        if str(request_asset_id) != str(bar_asset_id):
            raise serializers.ValidationError({
                "asset": "bar data asset pk must be same as url params "
                "`asset_id`"
            })

        return data
