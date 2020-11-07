from rest_framework import serializers

from .models import Asset, AssetClass, Exchange


class AssetSerializer(serializers.ModelSerializer):
    """Serializer for a user of the system."""

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
