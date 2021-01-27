from rest_framework import serializers
from server.assets.models import Asset
from server.core.models import Strategy
from server.users.models import User
from server.users.serializers import UserSerializer

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for listing/retrieving an order placed by a user of Alpaca."""

    user = UserSerializer(fields=("id", "first_name", "last_name"))
    symbol = serializers.SlugRelatedField(
        queryset=Asset.objects.all(),
        slug_field="symbol",
    )
    strategy = serializers.SlugRelatedField(
        queryset=Strategy.objects.all(),
        slug_field="type",
    )
    client_order_id = serializers.UUIDField(format='hex_verbose')
    status = serializers.CharField(source='get_status_display')
    side = serializers.CharField(source='get_side_display')
    type = serializers.CharField(source='get_type_display')
    time_in_force = serializers.CharField(source='get_time_in_force_display')
    order_class = serializers.CharField(source='get_order_class_display')

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = [f.name for f in Order._meta.get_fields()]


class OrderPostSerializer(serializers.ModelSerializer):
    """Serializer for posting an order to the Alpaca api."""

    # TO DO

    class Meta:
        model = Order
        fields = (
            'symbol', 'qty', 'side', 'type', 'time_in_force', 'limit_price',
            'stop_price', 'trail_price', 'trail_percent', 'extended_hours',
            'client_order_id', 'order_class', 'take_profit', 'stop_loss'
        )


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating/updating an order object returned from Alpaca api.
    """

    user = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all()
    )
    symbol = serializers.SlugRelatedField(
        queryset=Asset.objects.all(),
        slug_field="symbol",
    )
    strategy = serializers.PrimaryKeyRelatedField(
        queryset=Strategy.objects.all(),
        required=False
    )
    client_order_id = serializers.UUIDField(format='hex_verbose')

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

        if (is_stop_limit or is_limit) and not has_limit_price:
            raise serializers.ValidationError({'limit_price': [
                'Field is required if `type` is `stop_limit` or `limit`'
            ]})
        if (is_stop or is_stop_limit) and not has_stop_price:
            raise serializers.ValidationError({'stop_price': [
                'Field is required if `type` is `stop` or `stop_limit`'
            ]})
        if is_trailing_stop and not (has_trail_percent or has_trail_price):
            error_message = [
                "Either `trail_price` or `trail_percentage` is required if "
                "`type` is `trailing_stop`"
            ]
            raise serializers.ValidationError({
                'trail_percent': error_message,
                'trail_price': error_message
            })
        return data
