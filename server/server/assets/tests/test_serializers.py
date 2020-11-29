import uuid

from django.test import TestCase
from django.test.client import RequestFactory
from server.users.serializers import UserSerializer
from server.users.tests.factories import AdminFactory

from .factories import AssetClassFactory, AssetFactory, ExchangeFactory
from .models import Asset, AssetClass, Exchange
from .serializers import (AssetClassSerializer, AssetSerializer,
                          ExchangeSerializer)


class ExchangeSerializerTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.admin = AdminFactory()
        cls.request = RequestFactory().get('/')
        cls.request.user = cls.admin

    def test_view_exchange(self):
        """Exchange data is serialized correctly."""
        exchange = ExchangeFactory()
        data = ExchangeSerializer(
            exchange, context={'request': self.request}
        ).data

        self.assertEqual(data['name'], exchange.name)
        self.assertEqual(data['alt_name'], exchange.alt_name)
        self.assertEqual(data['is_active'], True)

    def test_save_exchange(self):
        """Exchange data is saved correctly."""
        data = {
            "name": "Exchange",
            "alt_name": "Alt Exchange Name",
            "is_active": True,
        }

        serializer = ExchangeSerializer(
            data=data, context={'request': self.request}
        )
        self.assertTrue(serializer.is_valid())
        exchange = serializer.save()

        self.assertEqual(Exchange.objects.count(), 1)
        self.assertEqual(exchange.name, data['name'])
        self.assertEqual(exchange.alt_name, data['alt_name'])
        self.assertTrue(exchange.is_active)


class AssetClassSerializerTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.admin = AdminFactory()
        cls.request = RequestFactory().get('/')
        cls.request.user = cls.admin

    def test_view_asset_class(self):
        """Asset class data is serialized correctly."""
        asset_class = AssetClassFactory()
        data = AssetClassSerializer(
            asset_class, context={'request': self.request}
        ).data

        self.assertEqual(data['name'], asset_class.name)
        self.assertEqual(data['alt_name'], asset_class.alt_name)
        self.assertTrue(data['is_active'])

    def test_save_asset_class(self):
        """Asset class data is saved correctly."""
        data = {
            "name": "Asset Class",
            "alt_name": "Alt Asset Class Name",
            "is_active": True,
        }

        serializer = AssetClassSerializer(
            data=data, context={'request': self.request}
        )
        self.assertTrue(serializer.is_valid())
        asset_class = serializer.save()

        self.assertEqual(AssetClass.objects.count(), 1)
        self.assertEqual(asset_class.name, data['name'])
        self.assertEqual(asset_class.alt_name, data['alt_name'])
        self.assertTrue(asset_class.is_active)


class AssetSerializerTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.admin = AdminFactory()
        cls.request = RequestFactory().get('/')
        cls.request.user = cls.admin
        cls.asset_class = AssetClassFactory()
        cls.exchange = ExchangeFactory()

    def test_view_asset(self):
        """Asset data is serialized correctly."""
        asset = AssetFactory()
        data = AssetSerializer(asset, context={'request': self.request}).data

        self.assertEqual(Asset.objects.count(), 1)
        self.assertEqual(data['id'], asset.id)
        self.assertEqual(data['asset_class'], asset.asset_class)
        self.assertTrue(data['easy_to_borrow'])
        self.assertEqual(data['exchange'], asset.exchange)
        self.assertTrue(data['marginable'])
        self.assertTrue(data['shortable'])
        self.assertEqual(data['status'], asset.status)
        self.assertEqual(data['symbol'], asset.symbol)
        self.assertTrue(data['tradable'])

    def test_save_asset(self):
        """Asset data is saved correctly."""
        asset_uuid = uuid.uuid4()
        data = {
            'id': str(asset_uuid),
            'name': 'Asset Name',
            'asset_class': self.asset_class.name,
            'easy_to_borrow': True,
            'exchange': self.exchange.name,
            'marginable': True,
            'shortable': True,
            'status': Asset.ACTIVE,
            'symbol': 'SYMBOL',
            'tradable': True,
        }

        serializer = AssetSerializer(
            data=data, context={'request': self.request}
        )
        self.assertTrue(serializer.is_valid())
        asset = serializer.save()

        self.assertEqual(Asset.objects.count(), 1)
        self.assertEqual(asset.id, data['id'])
        self.assertEqual(asset.asset_class, data['asset_class'])
        self.assertTrue(asset.easy_to_borrow)
        self.assertEqual(asset.exchange, data['exchange'])
        self.assertTrue(asset.marginable)
        self.assertTrue(asset.shortable)
        self.assertEqual(asset.status, data['status'])
        self.assertEqual(asset.symbol, data['symbol'])
        self.assertTrue(asset.tradable)
