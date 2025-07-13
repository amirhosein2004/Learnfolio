from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path('admin/', admin.site.urls), # admin 
    path('api/auth/', include('accounts.urls')), # accounts app 
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