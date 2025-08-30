from django.urls import path
from accounts.api.v1.views.profile_views import (
    UserProfileAPIView,
    AdminProfileAPIView,
)



urlpatterns = [
    # profile
    path('/', UserProfileAPIView.as_view(), name='user_profile'),
    path('admin/', AdminProfileAPIView.as_view(), name='admin_profile'),
]