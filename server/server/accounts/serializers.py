from rest_framework import serializers
from server.assets.models import Asset
from server.users.models import User
from server.users.serializers import UserSerializer

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    """Serializer for account information of a user of Alpaca."""

    id = serializers.UUIDField(format='hex_verbose')
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Account
        fields = '__all__'

    def to_representation(self, instance):
        """Return fully serialized users."""
        ret = super().to_representation(instance)
        ret['user'] = UserSerializer(
            fields=("id", "first_name", "last_name")
        ).data
        return ret
