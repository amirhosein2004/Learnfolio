from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Accounts app URLs
    path('api/accounts/', include('accounts.urls')),

    # Blog app URLs
    path('api/blog/', include('blog.urls')),
]

# active in dev 
if settings.DEBUG:
    urlpatterns += [
        # Raw OpenAPI schema endpoint
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

        # Swagger UI documentation
        path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

        # Redoc documentation (more professional and user-friendly)
        path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]