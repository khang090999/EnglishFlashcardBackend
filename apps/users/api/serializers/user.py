from apps.core.api.serializers import ModelBaseSerializer

from ... import models


class UserSerializer(ModelBaseSerializer):
    """Serializer for representing `User`."""

    class Meta:
        model = models.User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "avatar",
            "last_login",
            "created",
            "modified",
        )
        read_only_fields = (
            "email",
            "last_login",
            "created",
            "modified",
        )
