from django.urls import path
from accounts.api.v1.views.password_views import (
    RequestPasswordResetAPIView,
    OTPVerificationPasswordResetAPIView,
    LinkVerificationPasswordResetAPIView,
    ResetPasswordAPIView,
    FirstTimePasswordAPIView,
    ChangePasswordAPIView,
)

urlpatterns = [
    # password
    path('request-password-reset/', RequestPasswordResetAPIView.as_view(), name='request_password_reset'),
    path('verify-otp/', OTPVerificationPasswordResetAPIView.as_view(), name='password_verify_otp'),
    path('verify-link/', LinkVerificationPasswordResetAPIView.as_view(), name='password_verify_link'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset_password'),
    path('first-time-password/', FirstTimePasswordAPIView.as_view(), name='first_time_password'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='change_password'),
]
