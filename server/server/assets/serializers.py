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
        request_asset = self.context['request'].GET
        print('\n\nrequest_asset', request_asset)
        bar_asset = data.asset.id

        if request_asset != bar_asset:
            raise serializers.ValidationError({
                "asset": "bar data asset must be same asset as asset url "
                "endpoint",
            })

        return data
