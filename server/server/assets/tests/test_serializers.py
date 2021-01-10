import uuid

from django.test import TestCase
from django.test.client import RequestFactory
from server.assets.models import Asset, AssetClass, Bar, Exchange
from server.assets.serializers import (AssetClassSerializer, AssetSerializer,
                                       BarSerializer, ExchangeSerializer)
from server.users.tests.factories import AdminFactory

from .factories import (AssetClassFactory, AssetFactory, BarFactory,
                        ExchangeFactory)


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

    def test_create_exchange(self):
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

    def test_update_exchange(self):
        """Exchange data is updated correctly."""
        exchange = ExchangeFactory(name='Old Exchange Name')
        serializer = ExchangeSerializer(
            exchange,
            data={'name': 'New Exchange Name'},
            partial=True,
            context={'request': self.request}
        )

        self.assertTrue(serializer.is_valid())
        serializer.save()

        exchange.refresh_from_db()
        self.assertEqual(exchange.name, 'New Exchange Name')


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

    def test_create_asset_class(self):
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

    def test_update_asset_class(self):
        """Asset class data is updated correctly."""
        asset_class = AssetClassFactory(name='Old Asset Class Name')
        serializer = AssetClassSerializer(
            asset_class,
            data={'name': 'New Asset Class Name'},
            partial=True,
            context={'request': self.request}
        )

        self.assertTrue(serializer.is_valid())
        serializer.save()

        asset_class.refresh_from_db()
        self.assertEqual(asset_class.name, 'New Asset Class Name')


class AssetSerializerTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.admin = AdminFactory()
        cls.request = RequestFactory().get('/')
        cls.request.user = cls.admin

    def setUp(self):
        self.asset_class = AssetClassFactory()
        self.exchange = ExchangeFactory()

    def test_view_asset(self):
        """Asset data is serialized correctly."""
        asset = AssetFactory(
            asset_class=self.asset_class,
            exchange=self.exchange
        )
        data = AssetSerializer(asset, context={'request': self.request}).data

        self.assertEqual(Asset.objects.count(), 1)
        self.assertEqual(data['id'], str(asset.id))
        self.assertEqual(data['asset_class'], asset.asset_class.name)
        self.assertTrue(data['easy_to_borrow'])
        self.assertEqual(data['exchange'], asset.exchange.name)
        self.assertTrue(data['marginable'])
        self.assertTrue(data['shortable'])
        self.assertEqual(data['status'], asset.status)
        self.assertEqual(data['symbol'], asset.symbol)
        self.assertTrue(data['tradable'])

    def test_create_asset(self):
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
        self.assertEqual(str(asset.id), data['id'])
        self.assertEqual(asset.asset_class.name, data['asset_class'])
        self.assertTrue(asset.easy_to_borrow)
        self.assertEqual(asset.exchange.name, data['exchange'])
        self.assertTrue(asset.marginable)
        self.assertTrue(asset.shortable)
        self.assertEqual(asset.status, data['status'])
        self.assertEqual(asset.symbol, data['symbol'])
        self.assertTrue(asset.tradable)

    def test_update_asset(self):
        """Asset data is updated correctly."""
        asset = AssetFactory(
            name='Old Asset Name',
            asset_class=self.asset_class,
            exchange=self.exchange
        )
        serializer = AssetSerializer(
            asset,
            data={'name': 'New Asset Name'},
            partial=True,
            context={'request': self.request}
        )

        self.assertTrue(serializer.is_valid())
        serializer.save()

        asset.refresh_from_db()
        self.assertEqual(asset.name, 'New Asset Name')


class BarSerializerTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.admin = AdminFactory()
        cls.request = RequestFactory().get('/')
        cls.request.user = cls.admin

    def setUp(self):
        self.asset = AssetFactory(symbol="AAPL")

    def test_view_bar(self):
        """Bar data is serialized correctly."""
        bar = BarFactory(asset=self.asset)
        data = BarSerializer(bar, context={'request': self.request}).data

        self.assertEqual(Bar.objects.count(), 1)
        self.assertEqual(data['asset'], self.asset.symbol)
        self.assertEqual(data['t'], bar.t)
        self.assertEqual(float(data['o']), bar.o)
        self.assertEqual(float(data['h']), bar.h)
        self.assertEqual(float(data['l']), bar.l)
        self.assertEqual(float(data['c']), bar.c)
        self.assertEqual(data['v'], bar.v)

    def test_create_bar(self):
        """Bar data is saved correctly."""
        data = {
            "asset": self.asset.symbol,
            "t": 2100000000,
            "o": 100.01,
            "h": 110.05,
            "l": 99.05,
            "c": 105.01,
            "v": 200000
        }

        serializer = BarSerializer(
            data=data,
            context={'request': self.request, 'asset_id': self.asset.id}
        )

        self.assertTrue(serializer.is_valid())
        bar = serializer.save()

        self.assertEqual(Bar.objects.count(), 1)
        self.assertEqual(data['asset'], bar.asset.symbol)
        self.assertEqual(data['t'], bar.t)
        self.assertEqual(data['o'], float(bar.o))
        self.assertEqual(data['h'], float(bar.h))
        self.assertEqual(data['l'], float(bar.l))
        self.assertEqual(data['c'], float(bar.c))
        self.assertEqual(data['v'], bar.v)

    def test_create_bar_invalid(self):
        """
        Errors are raised if request params asset_id is not the same as the data
        asset pk.
        """
        new_asset = AssetFactory()
        data = {
            "asset": new_asset.symbol,
            "t": 2100000000,
            "o": 100.01,
            "h": 110.05,
            "l": 99.05,
            "c": 105.01,
            "v": 200000
        }

        serializer = BarSerializer(
            data=data,
            context={'request': self.request, 'asset_id': self.asset.id}
        )

        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["asset"][0],
            "bar data asset pk must be same as url params `asset_id`"
        )

    def test_update_bar(self):
        """Bar data can be partially updated."""
        bar = BarFactory(
            c=100.05,
            asset=self.asset,
        )
        serializer = BarSerializer(
            bar,
            data={'c': 105.10},
            partial=True,
            context={'request': self.request, 'asset_id': self.asset.id}
        )

        self.assertTrue(serializer.is_valid())
        serializer.save()

        bar.refresh_from_db()
        self.assertEqual(float(bar.c), 105.10)
