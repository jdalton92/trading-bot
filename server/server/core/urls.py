from rest_framework.routers import DefaultRouter

from .views import StrategyView

router = DefaultRouter()

router.register(r"strategies/", StrategyView, basename="strategies")

urlpatterns = router.urls
