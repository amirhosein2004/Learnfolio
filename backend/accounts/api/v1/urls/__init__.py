from django.urls import path, include

urlpatterns = [
    path('auth/', include('accounts.api.v1.urls.auth_urls')),
    path('password/', include('accounts.api.v1.urls.password_urls')),
    path('profile/', include('accounts.api.v1.urls.profile_urls')),
]
