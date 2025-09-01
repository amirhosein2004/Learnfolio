from django.urls import path
from accounts.api.v1.views.auth_views import (
    IdentitySubmissionAPIView,
    OTPOrVerificationAPIView,
    ResendOTPOrLinkAPIView,
    LinkVerificationAPIView,
    PasswordLoginAPIView,
    LogoutAPIView,
    CustomTokenRefreshView,
)

urlpatterns = [
    # auth
    path('submit-identity/', IdentitySubmissionAPIView.as_view(), name='submit_identity'),
    path('verify-otp/', OTPOrVerificationAPIView.as_view(), name='verify_otp'),
    path('verify-link/', LinkVerificationAPIView.as_view(), name='verify_link'),
    path('resend-otp-or-link/', ResendOTPOrLinkAPIView.as_view(), name='resend_otp_or_link'),
    path('login-password/', PasswordLoginAPIView.as_view(), name='login_password'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'), # path refresh, access token
]
