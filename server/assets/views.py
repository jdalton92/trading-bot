from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .models import Asset, AssetClass, Bar, Exchange
from .serializers import (
    AssetClassSerializer,
    AssetSerializer,
    BarSerializer,
    ExchangeSerializer,
)


class AssetView(viewsets.ModelViewSet):
    def get_queryset(self, *args, **kwargs):
        """Return assets to requesting user."""
        return Asset.objects.all()

    def get_serializer_class(self):
        """
        Instantiates and returns the serializer that the asset view requires.
        """
        return AssetSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that the asset view
        requires.
        """
        if self.action in ["list", "retrieve"]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class AssetClassView(viewsets.ModelViewSet):
    def get_queryset(self, *args, **kwargs):
        """Return asset classes to requesting user."""
        return AssetClass.objects.all()

    def get_serializer_class(self):
        """
        Instantiates and returns the serializer that the asset class view
        requires.
        """
        return AssetClassSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that the asset class
        view requires.
        """
        if self.action in ["list", "retrieve"]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class ExchangeView(viewsets.ModelViewSet):
    def get_queryset(self, *args, **kwargs):
        """Return exchanges to requesting user."""
        return Exchange.objects.all()

    def get_serializer_class(self):
        """
        Instantiates and returns the serializer that the exchange view requires.
        """
        return ExchangeSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that the exchanges view
        requires.
        """
        if self.action in ["list", "retrieve"]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class BarView(viewsets.ModelViewSet):
    def get_queryset(self, *args, **kwargs):
        """Return bars to requesting user."""
        queryset = Bar.objects.visible(self.kwargs["asset_id"])
        start = self.request.query_params.get("start")
        end = self.request.query_params.get("end")

        if (start and not end) or (not start and end):
            raise ValidationError("You must include both `start` and `end` params")

        if start and end:
            queryset = queryset.filter(t__gte=start, t__lt=end)

        return queryset

    def get_serializer_class(self):
        """
        Instantiates and returns the serializer that the bar view requires.
        """
        return BarSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that the bar view
        requires.
        """
        if self.action in ["list", "retrieve"]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        """Add asset symbol from endpoint to bar data."""
        data = request.data
        data["asset"] = get_object_or_404(Asset, pk=self.kwargs.get("asset_id")).symbol
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
