import debug_toolbar
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from .auth.views import CustomAuthToken, LoginView

default_urls = [
    url(r'^admin/', admin.site.urls),
    url(r'^__debug__/', include(debug_toolbar.urls)),
]

auth_urls = [
    path(r'register/', LoginView.as_view(), name="register"),
    path(r'api-auth-token/', CustomAuthToken.as_view(), name="api-auth-token"),
]

app_urls = [
    path(r'users/', include('api.users.urls')),
    path(r'assets/', include('api.assets.urls')),
]

versioned_urls = DefaultRouter.urls
non_versioned_urls = sum([
    default_urls,
    auth_urls
], list())

urlpatterns = [
    url(r'^', include(DefaultRouter(trailing_slash=True).urls)),
    url(r'^v1/', include((app_urls, 'v1'), namespace='v1')),
] + non_versioned_urls
