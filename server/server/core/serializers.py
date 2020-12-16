from rest_framework import serializers


class DynamicModelSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        """Dynamically add or exclude the fields to be serialized."""
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
