from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from server.core.permissions import IsAdminOrOwner

from .models import Account
from .serializers import AccountSerializer


class AccountView(viewsets.ModelViewSet):

    def get_queryset(self, *args, **kwargs):
        """Return accounts to requesting user."""
        return Account.objects.visible(self.request.user)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that the account view
        requires.
        """
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAdminOrOwner]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        return AccountSerializer
