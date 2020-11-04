from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for a user of the system."""

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'is_active', 'is_admin', 'date_joined', 'last_login'
        )
