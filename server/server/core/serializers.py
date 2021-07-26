from rest_framework import serializers
from server.assets.models import Asset
from server.users.models import User
from server.users.serializers import UserSerializer

from .models import Strategy


class StrategySerializer(serializers.ModelSerializer):
    """Serializer for listing/retrieving a user strategy."""

    user = UserSerializer(fields=("id", "first_name", "last_name"))
    asset = serializers.SlugRelatedField(
        queryset=Asset.objects.all(),
        slug_field="symbol",
    )

    class Meta:
        model = Strategy
        fields = (
            "user",
            "type",
            "asset",
            "start_date",
            "end_date",
            "trade_value",
            "stop_loss_amount",
            "stop_loss_percentage",
            "take_profit_amount",
            "take_profit_percentage",
            "is_active",
            "timeframe",
        )
        read_only_fields = fields


class StrategyCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating a user strategy."""

    user = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(), queryset=User.objects.all()
    )
    asset = serializers.SlugRelatedField(
        queryset=Asset.objects.all(),
        slug_field="symbol",
    )

    class Meta:
        model = Strategy
        fields = (
            "user",
            "type",
            "asset",
            "start_date",
            "end_date",
            "trade_value",
            "stop_loss_amount",
            "stop_loss_percentage",
            "take_profit_amount",
            "take_profit_percentage",
            "is_active",
            "timeframe",
        )

    def validate(self, data):
        """Validate strategy data."""
        stop_loss_amount = data.get("stop_loss_amount")
        stop_loss_percentage = data.get("stop_loss_percentage")
        take_profit_amount = data.get("take_profit_amount")
        take_profit_percentage = data.get("take_profit_percentage")

        if stop_loss_amount and stop_loss_percentage:
            error_message = [
                "Enter either `stop_loss_amount` or `stop_loss_percentage`, but"
                " not both"
            ]
            raise serializers.ValidationError(
                {
                    "stop_loss_amount": error_message,
                    "stop_loss_percentage": error_message,
                }
            )

        if take_profit_amount and take_profit_percentage:
            error_message = [
                "Enter either `take_profit_amount` or `take_profit_percentage`,"
                " but not both"
            ]
            raise serializers.ValidationError(
                {
                    "take_profit_amount": error_message,
                    "take_profit_percentage": error_message,
                }
            )

        return data
