from rest_framework import generics, mixins, permissions

from ... import models
from .. import serializers


class ProfileViewSet(generics.RetrieveAPIView):
    """Viewset for managing current user."""

    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # To avoid creating patch method
    # For more info checkout UpdateModelWithoutPatchMixin in core app
    put = mixins.UpdateModelMixin.update
    perform_update = mixins.UpdateModelMixin.perform_update

    def get_object(self):
        """Restrict to current user."""
        return self.request.user

    def get_queryset(self):
        """Restrict since only get_object should be used."""
        return models.User.objects.none()
