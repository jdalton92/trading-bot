import uuid

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from server.assets.models import Asset, AssetClass, Exchange
from server.assets.tests.factories import (AssetClassFactory, AssetFactory,
                                           ExchangeFactory)
from server.users.tests.factories import UserFactory


class ExchangeViewTests(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.exchange = ExchangeFactory()
        self.data = {
            'name': 'Exchange Name',
            'alt_name': 'Exchange Alt Name',
            'is_active': True
        }
        self.client.force_authenticate(self.user)

    def test_list_exchanges(self):
        """Exchanges are listed."""
        response = self.client.get(reverse("v1:exchanges-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_exchanges(self):
        """Exchanges can be created."""
        response = self.client.post(reverse("v1:exchanges-list"), self.data)
        exchange = Exchange.objects.filter(id=self.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exchange.exists())
        self.assertEqual(exchange.name, self.data['name'])
        self.assertEqual(exchange.alt_name, self.data['alt_name'])
        self.assertEqual(exchange.is_active, self.data['is_active'])

    def test_partial_update_exchanges(self):
        """Exchanges can be partially updated."""
        data = {"name": "New Exchange Name"}

        response = self.client.patch(
            reverse("v1:exchanges-detail", args=[self.exchange.pk]),
            data
        )
        self.exchange.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.exchange.name, data["name"])

    def test_delete_exchanges(self):
        """Exchanges can be deleted."""
        response = self.client.delete(
            reverse("v1:exchanges-detail", args=[self.exchange.pk])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            Exchange.objects.filter(pk=self.exchange.pk).exists()
        )


class AssetClassViewTests(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.asset_class = AssetClassFactory()
        self.data = {
            'name': 'Asset Class Name',
            'alt_name': 'Asset Class Alt Name',
            'is_active': True
        }
        self.client.force_authenticate(self.user)

    def test_list_asset_class(self):
        """Asset class are listed."""
        response = self.client.get(reverse("v1:asset-classes-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_asset_class(self):
        """Asset class can be created."""
        response = self.client.post(reverse("v1:asset-classes-list"), self.data)
        asset_class = AssetClass.objects.filter(id=self.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(asset_class.exists())
        self.assertEqual(asset_class.name, self.data['name'])
        self.assertEqual(asset_class.alt_name, self.data['alt_name'])
        self.assertEqual(asset_class.is_active, self.data['is_active'])

    def test_partial_update_asset_class(self):
        """Asset class can be partially updated."""
        data = {"name": "New Asset Class Name"}

        response = self.client.patch(
            reverse("v1:asset-classes-detail", args=[self.asset_class.pk]),
            data
        )
        self.asset_class.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.asset_class.name, data["name"])

    def test_delete_asset_class(self):
        """Asset class can be deleted."""
        response = self.client.delete(
            reverse("v1:asset-classes-detail", args=[self.asset_class.pk])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            AssetClass.objects.filter(pk=self.asset_class.pk).exists()
        )


class AssetViewTests(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.exchange = ExchangeFactory()
        self.asset_class = AssetClassFactory()
        self.asset_1 = AssetFactory(
            exchange=self.exchange,
            asset_class=self.asset_class
        )
        self.asset_2 = AssetFactory(
            exchange=self.exchange,
            asset_class=self.asset_class
        )
        self.data = {
            'id': str(uuid.uuid4()),
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
        self.client.force_authenticate(self.user)

    def test_list_assets(self):
        """Assets are listed."""
        response = self.client.get(reverse("v1:assets-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_asset(self):
        """Assets can be created."""
        response = self.client.post(reverse("v1:users-list"), self.data)
        asset = Asset.objects.filter(id=self.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(asset.exists())
        self.assertEqual(asset.name, self.data['name'])
        self.assertEqual(asset.asset_class.name, self.data['asset_class'])
        self.assertEqual(asset.easy_to_borrow, self.data['easy_to_borrow'])
        self.assertEqual(asset.exchange.name, self.data['exchange'])
        self.assertEqual(asset.marginable, self.data['marginable'])
        self.assertEqual(asset.shortable, self.data['shortable'])
        self.assertEqual(asset.status, self.data['status'])
        self.assertEqual(asset.symbol, self.data['symbol'])
        self.assertEqual(asset.tradable, self.data['tradable'])

    def test_asset_partial_update(self):
        """Assets can be partially updated."""
        data = {"name": "New Name"}

        response = self.client.patch(
            reverse("v1:assets-detail", args=[self.asset_1.pk]),
            data
        )
        self.asset_1.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.asset_1.name, data["name"])

    def test_asset_partial_update_asset_class(self):
        """Assets can asset class updated."""
        new_asset_class = AssetClassFactory()
        data = {"asset_class": new_asset_class.name}

        response = self.client.patch(
            reverse("v1:assets-detail", args=[self.asset_1.pk]),
            data
        )
        self.asset_1.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.asset_1.asset_class.name, data["asset_class"])

    def test_asset_partial_update_exchange(self):
        """Assets can have exchange updated."""
        new_exchange = ExchangeFactory()
        data = {"exchange": new_exchange.name}

        response = self.client.patch(
            reverse("v1:assets-detail", args=[self.asset_1.pk]),
            data
        )
        self.asset_1.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.asset_1.exchange.name, data["exchange"])

    def test_delete_asset(self):
        """Assets can be deleted."""
        response = self.client.delete(
            reverse("v1:assets-detail", args=[self.asset_1.pk])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Asset.objects.filter(pk=self.asset_1.pk).exists())
