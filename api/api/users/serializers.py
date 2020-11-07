from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for a user of the system."""

    class Meta:
        model = User
        fields = '__all__'
