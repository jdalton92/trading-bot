from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .models import Asset, AssetClass, Exchange
from .serializers import (AssetBulkCreateSerializer, AssetClassSerializer,
                          AssetSerializer, ExchangeSerializer)


class AssetView(viewsets.ModelViewSet):

    def get_queryset(self, *args, **kwargs):
        return Asset.objects.all()

    def get_serializer_class(self):
        if self.action in ['bulkadd']:
            return AssetClassSerializer
        else:
            return AssetSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that the asset view
        requires.
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(
        detail=False,
        methods=['post']
    )
    def bulkadd(self, *args, **kwargs):
        """
        Bulk create assets from response list in form of response from Alpaca
        api.
        """
        data = self.request.data
        if not isinstance(data, list):
            data = [data]
        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class AssetClassView(viewsets.ModelViewSet):

    def get_queryset(self, *args, **kwargs):
        return AssetClass.objects.all()

    def get_serializer_class(self):
        return AssetClassSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that the asset class
        view requires.
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class ExchangeView(viewsets.ModelViewSet):

    def get_queryset(self, *args, **kwargs):
        return Exchange.objects.all()

    def get_serializer_class(self):
        return ExchangeSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that the exchanges view
        requires.
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
