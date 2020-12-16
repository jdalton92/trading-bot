from django.contrib.auth.models import Group
from rest_framework import serializers
from server.core.serializers import DynamicModelSerializer

from .models import User


class GroupSerializer(serializers.ModelSerializer):
    """Serializer for groups of the system."""

    class Meta:
        model = Group
        fields = "__all__"


class UserSerializer(DynamicModelSerializer):
    """Serializer for a user of the system."""

    groups = serializers.SlugRelatedField(
        queryset=Group.objects.all(),
        slug_field="name",
        many=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = User
        fields = (
            "first_name", "last_name", "email", "groups", "is_active",
            "is_staff", "is_superuser", "last_login", "date_joined"
        )

    def to_representation(self, instance):
        """Return fully serialized groups."""
        ret = super().to_representation(instance)
        ret['groups'] = GroupSerializer(instance.groups, many=True).data
        return ret
