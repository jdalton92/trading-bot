from rest_framework.routers import DefaultRouter

from .views import AssetClassView, AssetView, ExchangeView

router = DefaultRouter()

router.register(r'', AssetView, basename='assets')
router.register(r'classes', AssetClassView, basename='assetclasses')
router.register(r'exchanges', ExchangeView, basename='exchanges')

urlpatterns = router.urls
