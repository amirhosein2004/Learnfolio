from django.urls import path
from accounts.api.v1.views.profile_views import (
    UserProfileAPIView,
    AdminProfileAPIView,
    UserUpdateEmailOrPhoneAPIView,
    VerifyOTPUserUpdatePhoneAPIView,
    ConfirmationLinkUserUpdateEmailAPIView
)



urlpatterns = [
    # profile
    path("me/", UserProfileAPIView.as_view(), name="user_profile_me"),
    path("admin/me/", AdminProfileAPIView.as_view(), name="admin_profile_me"),
    path("update-identity/", UserUpdateEmailOrPhoneAPIView.as_view(), name="user_update_identity"),
    path("update-phone/verify/", VerifyOTPUserUpdatePhoneAPIView.as_view(), name="user_update_phone_verify"),
    path("update-email/confirm/", ConfirmationLinkUserUpdateEmailAPIView.as_view(), name="user_update_email_confirm"),
]
