from rest_framework import serializers
from server.assets.models import Asset

from .models import Order, StopLoss, TakeProfit


class TakeProfitSerializer(serializers.ModelSerializer):
    """
    Serializer for take profit orders via Alpaca api.
    """

    class Meta:
        model = TakeProfit
        fields = '__all__'


class StopLossSerializer(serializers.ModelSerializer):
    """
    Serializer for stop loss orders via Alpaca api.
    """

    class Meta:
        model = StopLoss
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for an order placed by a user of Alpaca."""

    symbol = serializers.SlugRelatedField(
        queryset=Asset.objects.all(),
        slug_field="symbol",
    )
    client_order_id = serializers.UUIDField(format='hex_verbose')
    # take_profit = serializers.SlugRelatedField(
    #     queryset=TakeProfit.objects.all(),
    #     slug_field="limit_price",
    #     required=False,
    #     allow_null=True
    # )
    # stop_loss = serializers.SlugRelatedField(
    #     queryset=StopLoss.objects.all(),
    #     slug_field="stop_price",
    #     required=False,
    #     allow_null=True
    # )
    take_profit = TakeProfitSerializer()
    stop_loss = StopLossSerializer()

    class Meta:
        model = Asset
        fields = '__all__'

    def validate(self, data):
        """Validate conditionally required fields."""
        if (data.get('type') == Order.STOP_LIMIT or data.get('type') == Order.LIMIT
                and not data.get('limit_price')):
            raise serializers.ValidationError({'limit_price': [
                'Field is required if `type` is `stop_limit` or `limit`'
            ]})
        if (data.get('type') == Order.STOP or data.get('type') == Order.STOP_LIMIT
                and not data.get('stop_price')):
            raise serializers.ValidationError({'stop_price': [
                'Field is required if `type` is `stop` or `stop_limit`'
            ]})
        if (data.get('type') == Order.TRAILING_STOP and not (data.get('trail_percent') or data.get('trail_price'))):
            raise serializers.ValidationError(
                'Either `trail_price` or `trail_percentage` is required if `type` is `trailing_stop`'
            )
        return data
