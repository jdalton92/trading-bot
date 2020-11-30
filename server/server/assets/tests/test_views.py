from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from server.asset.tests.factories import (AssetClassFactory, AssetFactory,
                                          ExchangeFactory)


class AssetViewTests(APITestCase):

    def setUp(self):
        self.asset = AssetFactory()

    # TO DO


class AssetClassViewTests(APITestCase):

    def setUp(self):
        self.asset_class = AssetClassFactory()

    # TO DO


class ExchangeViewTests(APITestCase):

    def setUp(self):
        self.exchange = ExchangeFactory()

    # TO DO
