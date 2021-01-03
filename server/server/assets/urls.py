from rest_framework.routers import DefaultRouter

from .views import AssetClassView, AssetView, BarView, ExchangeView

router = DefaultRouter()

router.register(r'assets', AssetView, basename='assets')
router.register(
    r'assets/(?P<asset_id>[0-9a-f-]+)/bars',
    BarView,
    basename='asset-bars'
)
router.register(r'assetclasses', AssetClassView, basename='asset-classes')
router.register(r'exchanges', ExchangeView, basename='exchanges')

urlpatterns = router.urls
