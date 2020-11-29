import uuid

from django.test import TestCase
from server.assets.models import Asset, AssetClass, Exchange


class ExchangeTests(TestCase):

    def test_create_exchange(self):
        """Exchange object can be created."""
        exchange = Exchange(
            name='Exchange',
            alt_name='Alt Exchange Name',
        )

        self.assertIn(exchange, Exchange.objects.all())
        self.assertEqual(exchange.name, 'Exchange')
        self.assertEqual(exchange.alt_name, 'Alt Exchange Name')
        self.assertTrue(exchange.is_active)


class AssetClassTests(TestCase):

    def test_create_asset_class(self):
        """Asset class object can be created."""
        asset_class = AssetClass(
            name='Asset Class',
            alt_name='Alt Asset Class Name',
        )

        self.assertIn(asset_class, AssetClass.objects.all())
        self.assertEqual(asset_class.name, 'Asset Class')
        self.assertEqual(asset_class.alt_name, 'Alt Asset Class Name')
        self.assertTrue(asset_class.is_active)


class AssetTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.asset_class = AssetClass(
            name='Asset Class',
            alt_name='Alt Asset Class Name',
        )
        cls.exchange = Exchange(
            name='Exchange',
            alt_name='Alt Exchange Name',
        )

    def test_create_asset(self):
        """Asset object can be created."""
        asset_uuid = uuid.uuid4()
        asset = Asset(
            id=asset_uuid,
            name='Asset Name',
            asset_class=self.asset_class,
            easy_to_borrow=True,
            exchange=self.exchange,
            marginable=True,
            shortable=True,
            status=Asset.ACTIVE,
            symbol='SYMBOL',
            tradable=True,
        )
        asset.save()

        self.assertIn(asset, Asset.objects.all())
        self.assertEqual(asset.id, str(asset_uuid))
        self.assertEqual(asset.name, 'Asset Name')
        self.assertEqual(asset.asset_class, self.asset_class.pk)
        self.assertTrue(asset.easy_to_borrow)
        self.assertEqual(asset.exchange, self.exchange.pk)
        self.assertTrue(asset.marginable)
        self.assertTrue(asset.shortable)
        self.assertEqual(asset.status, Asset.ACTIVE)
        self.assertEqual(asset.symbol, 'SYMBOL')
        self.assertTrue(asset.tradable)
