from core.permissions import IsAdminOrOwner
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Order
from .serializers import OrderCreateSerializer, OrderSerializer


class OrderView(viewsets.ModelViewSet):
    def get_queryset(self, *args, **kwargs):
        """Return orders to requesting user."""
        return Order.objects.visible(self.request.user)

    def get_serializer_class(self):
        """
        Instantiates and returns the serializer that the order view requires.
        """
        if self.action in ["list", "retrieve"]:
            return OrderSerializer
        return OrderCreateSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that the order view
        requires.
        """
        if self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [IsAdminOrOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Auto add the requesting user."""
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """Auto add the requesting user."""
        serializer.save(user=self.request.user)
