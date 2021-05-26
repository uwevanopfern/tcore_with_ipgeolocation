from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


schema_view = get_schema_view(
    openapi.Info(
        title="TradeCore APIs Documentation",
        default_version="v1",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(
        "",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("admin/", admin.site.urls),
    path("api/v1", include("social_app.api.urls")),
    path("login/v1/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/v1/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/v1/", TokenVerifyView.as_view(), name="token_verify"),
]
