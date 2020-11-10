from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Asset, AssetClass, Exchange

# from .tasks import bulk_add_assets


class AssetSerializer(serializers.ModelSerializer):
    """Serializer for a user of the system."""

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


class AssetBulkCreateSerializer(serializers.Serializer):
    """
    Serializer for bulk creating assets returned from Alpaca api.
    """

    id = serializers.UUIDField(format='hex_verbose')
    class_name = serializers.SerializerMethodField()
    asset_class = serializers.SlugRelatedField(
        source='class_name',
        queryset=AssetClass.objects.all(),
        slug_field='name',
    )
    exchange = serializers.SlugRelatedField(
        queryset=Exchange.objects.all(),
        slug_field="name",
    )
    status = serializers.CharField(source='get_status_display')
    name = serializers.CharField()
    tradable = serializers.BooleanField()
    marginable = serializers.BooleanField()
    shortable = serializers.BooleanField()
    easy_to_borrow = serializers.BooleanField()
    symbol = serializers.CharField()

    def get_class_name(self, instance):
        """
        Get `class` field from Alpaca api response, and serialize to
        `class_name` field then validate as slugrelatedfield and saved to
        database under `asset_class` field
        """
        print('\n\nself', self)
        print('\n\ninstance', instance)
        return 'us_equity'

    # def validate(self, data):
    #     try:
    #         data["content_type"].get_object_for_this_type(
    #             id=data["asset_class"])
    #     except ObjectDoesNotExist:
    #         raise ValidationError("Object does not exist")
    #     return data

    # def save(self, *args, **kwargs):
    #     return bulk_add_assets.s(self.validated_data).delay
