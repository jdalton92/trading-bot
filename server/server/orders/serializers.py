from django.db import transaction
from rest_framework import mixins, serializers
from server.assets.models import Asset, AssetClass
from server.core.models import Strategy
from server.users.models import User
from server.users.serializers import UserSerializer

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for reading order objects returned from Alpaca."""

    user = UserSerializer(fields=("id", "first_name", "last_name"))
    symbol = serializers.SlugRelatedField(
        queryset=Asset.objects.all(),
        slug_field="symbol",
    )
    asset_class = serializers.SlugRelatedField(
        queryset=AssetClass.objects.all(),
        slug_field="name",
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

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = [f.name for f in Order._meta.get_fields()]

    def __init__(self, *args, **kwargs):
        """Dynamically add or exclude the fields to be serialized."""
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.legs.count():
            ret['legs'] = OrderSerializer(
                instance.legs,
                fields=('id', 'symbol', 'side', 'qty'),
                many=True,
            ).data
        return ret


class TakeProfitSerializer(serializers.Serializer):
    """Serializer for take profit params when posting an order to Alpaca api."""

    limit_price = serializers.DecimalField(max_digits=12, decimal_places=5)


class StopLossSerializer(serializers.Serializer):
    """Serializer for stop loss params when posting an order to Alpaca api."""

    stop_price = serializers.DecimalField(
        max_digits=12, decimal_places=5, required=False
    )
    limit_price = serializers.DecimalField(
        max_digits=12, decimal_places=5, required=False
    )

    def validate(self, data):
        """Validate conditionally required fields."""
        is_bracket = data.get('type') == Order.BRACKET
        has_limit_price = bool(data.get('limit_price'))
        if is_bracket and not has_limit_price:
            raise serializers.ValidationError({'limit_price': [
                'Field is required if `type` is `bracket`'
            ]})
        return data


class OrderPostSerializer(serializers.Serializer):
    """Serializer for posting an order to the Alpaca api."""

    symbol = serializers.CharField()
    qty = serializers.DecimalField(max_digits=12, decimal_places=5)
    side = serializers.ChoiceField(choices=Order.SIDE_CHOICES)
    type = serializers.ChoiceField(choices=Order.TYPE_CHOICES)
    time_in_force = serializers.ChoiceField(choices=Order.TIME_IN_FORCE_CHOICES)
    limit_price = serializers.DecimalField(
        max_digits=12, decimal_places=5, required=False
    )
    stop_price = serializers.DecimalField(
        max_digits=12, decimal_places=5, required=False
    )
    trail_price = serializers.DecimalField(
        max_digits=12, decimal_places=5, required=False
    )
    trail_percent = serializers.DecimalField(
        max_digits=12, decimal_places=5, required=False
    )
    extended_hours = serializers.BooleanField(default=False)
    client_order_id = serializers.UUIDField(format='hex_verbose')
    order_class = serializers.ChoiceField(
        choices=Order.ORDER_CLASS_CHOICES,
        default=Order.SIMPLE
    )
    take_profit = TakeProfitSerializer(required=False)
    stop_loss = StopLossSerializer(required=False)

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


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating/updating an order object returned from Alpaca api.
    """

    id = serializers.UUIDField(format='hex_verbose')
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
    legs = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = Order
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.legs.count():
            ret['legs'] = OrderSerializer(
                instance.legs,
                fields=('id', 'symbol', 'side', 'qty'),
                many=True,
            ).data
        return ret

    @transaction.atomic
    def create(self, validated_data):
        validated_data.pop('symbol', None)
        validated_data.pop('asset_class', None)
        return super().create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        validated_data.pop('symbol', None)
        validated_data.pop('asset_class', None)
        return super().update(instance, validated_data)
