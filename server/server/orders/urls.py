from rest_framework.routers import DefaultRouter

from .views import OrderView

router = DefaultRouter()

router.register(r'', OrderView, basename='orders')

urlpatterns = router.urls
