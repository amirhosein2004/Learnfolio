from django.urls import path

from .views.auth_views import (
    IdentitySubmissionAPIView,
    OTPOrVerificationAPIView,
    ResendOTPOrLinkAPIView,
    LinkVerificationAPIView,
    PasswordLoginAPIView,
    CustomTokenRefreshView
)

app_name = 'accounts'

urlpatterns = [
    path('auth/submit-identity/', IdentitySubmissionAPIView.as_view(), name='submit_identity'),
    path('auth/verify-otp/', OTPOrVerificationAPIView.as_view(), name='verify_otp'),
    path('auth/verify-link/', LinkVerificationAPIView.as_view(), name='verify_link'),
    path('auth/resend-otp-or-link/', ResendOTPOrLinkAPIView.as_view(), name='resend_otp_or_link'),
    path('auth/login-password/', PasswordLoginAPIView.as_view(), name='login_password'),
    path('auth/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'), # path refresh token
]