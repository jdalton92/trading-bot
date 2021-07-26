from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import User


class GroupSerializer(serializers.ModelSerializer):
    """Serializer for groups of the system."""

    class Meta:
        model = Group
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """Serializer for a user of the system."""

    groups = serializers.SlugRelatedField(
        queryset=Group.objects.all(),
        slug_field="name",
        many=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "groups",
            "is_active",
            "is_staff",
            "is_superuser",
            "last_login",
            "date_joined",
        )

    def __init__(self, *args, **kwargs):
        """Dynamically add or exclude the fields to be serialized."""
        fields = kwargs.pop("fields", None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def to_representation(self, instance):
        """Return fully serialized groups."""
        ret = super().to_representation(instance)
        if "groups" in self.fields:
            ret["groups"] = GroupSerializer(instance.groups, many=True).data
        return ret
