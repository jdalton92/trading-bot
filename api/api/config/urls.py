import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from .auth.views import CustomAuthToken, LoginView

urlpatterns = [
    # Default urls
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    # Auth urls
    path(r'register/', LoginView.as_view(), name="register"),
    path(r'api-auth-token/', CustomAuthToken.as_view(), name="api-auth-token"),
    # App urls
    path(r'users/', include('api.users.urls')),
    path(r'assets/', include('api.assets.urls')),
]
