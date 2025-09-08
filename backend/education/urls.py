from django.urls import path, include


urlpatterns = [
    path('v1/', include('education.api.v1.urls')),
]
