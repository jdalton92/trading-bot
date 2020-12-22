from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from server.core.permissions import IsAdminOrOwner

from .models import Strategy
from .serializers import StrategyCreateSerializer, StrategySerializer


class StrategyView(viewsets.ModelViewSet):

    def get_queryset(self, *args, **kwargs):
        """Return strategies to requesting user."""
        return Strategy.objects.visible(self.request.user)

    def get_serializer_class(self):
        """
        Instantiates and returns the serializer that the strategy view requires.
        """
        if self.action in ['list', 'retrieve']:
            return StrategySerializer
        return StrategyCreateSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that the strategy view
        requires.
        """
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAdminOrOwner]
        return [permission() for permission in permission_classes]
