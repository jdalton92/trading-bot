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
    """Serializer for listing/retrieving an order placed by a user of Alpaca."""

    symbol = serializers.SlugRelatedField(
        queryset=Asset.objects.all(),
        slug_field="symbol",
    )
    client_order_id = serializers.UUIDField(format='hex_verbose')
    take_profit = TakeProfitSerializer(read_only=True)
    stop_loss = StopLossSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = [f.name for f in Order._meta.get_fields()]


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating an order placed by a user of Alpaca."""

    symbol = serializers.SlugRelatedField(
        queryset=Asset.objects.all(),
        slug_field="symbol",
    )
    client_order_id = serializers.UUIDField(format='hex_verbose')
    take_profit = serializers.SlugRelatedField(
        queryset=TakeProfit.objects.all(),
        slug_field="limit_price",
        required=False,
        allow_null=True
    )
    stop_loss = serializers.SlugRelatedField(
        queryset=StopLoss.objects.all(),
        slug_field="stop_price",
        required=False,
        allow_null=True
    )

    class Meta:
        model = Order
        fields = '__all__'

    def validate(self, data):
        """Validate conditionally required fields."""
        order_type = data.get('type')
        is_stop_limit = order_type == Order.STOP_LIMIT
        is_stop = order_type == Order.STOP
        is_limit = order_type == Order.LIMIT
        is_trailing_stop = order_type == Order.TRAILING_STOP
        has_limit_price = bool(data.get('limit_price'))
        has_stop_price = bool(data.get('stop_price'))
        has_trail_percent = bool(data.get('trail_percent'))
        has_trail_price = bool(data.get('trail_price'))

        if (is_stop_limit or is_limit) and not is_limit_price:
            raise serializers.ValidationError({'limit_price': [
                'Field is required if `type` is `stop_limit` or `limit`'
            ]})
        if (is_stop or is_stop_limit) and not is_stop_price:
            raise serializers.ValidationError({'stop_price': [
                'Field is required if `type` is `stop` or `stop_limit`'
            ]})
        if is_trailing_stop and not (has_trail_percent or has_trail_price):
            raise serializers.ValidationError(
                """
                Either `trail_price` or `trail_percentage` is required if
                `type` is `trailing_stop`'
                """
            )
        return data
