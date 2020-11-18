from rest_framework.routers import DefaultRouter

from .views import AssetClassView, AssetView, ExchangeView

router = DefaultRouter()

router.register(r'assets', AssetView, basename='assets')
router.register(r'assetclasses', AssetClassView, basename='assetclasses')
router.register(r'exchanges', ExchangeView, basename='exchanges')

urlpatterns = router.urls
