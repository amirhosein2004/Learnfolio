from django.urls import path

from .views.auth_views import (
    IdentitySubmissionAPIView,
    OTPOrVerificationAPIView,
    ResendOTPOrLinkAPIView,
    LinkVerificationAPIView,
    PasswordLoginAPIView,
    LogoutAPIView,
    CustomTokenRefreshView,
)

from .views.password_views import (
    RequestPasswordResetAPIView,
    OTPVerificationPasswordResetAPIView,
    LinkVerificationPasswordResetAPIView,
    ResetPasswordAPIView,
    FirstTimePasswordAPIView,
    ChangePasswordAPIView,
)

app_name = 'accounts'

urlpatterns = [
    # auth
    path('auth/submit-identity/', IdentitySubmissionAPIView.as_view(), name='submit_identity'),
    path('auth/verify-otp/', OTPOrVerificationAPIView.as_view(), name='verify_otp'),
    path('auth/verify-link/', LinkVerificationAPIView.as_view(), name='verify_link'),
    path('auth/resend-otp-or-link/', ResendOTPOrLinkAPIView.as_view(), name='resend_otp_or_link'),
    path('auth/login-password/', PasswordLoginAPIView.as_view(), name='login_password'),
    path('auth/logout/', LogoutAPIView.as_view(), name='logout'),
    path('auth/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'), # path refresh, access token

    # password
    path('password/request-password-reset/', RequestPasswordResetAPIView.as_view(), name='request_password_reset'),
    path('password/verify-otp/', OTPVerificationPasswordResetAPIView.as_view(), name='password_verify_otp'),
    path('password/verify-link/', LinkVerificationPasswordResetAPIView.as_view(), name='password_verify_link'),
    path('password/reset-password/', ResetPasswordAPIView.as_view(), name='reset_password'),
    path('password/first-time-password/', FirstTimePasswordAPIView.as_view(), name='first_time_password'),
    path('password/change-password/', ChangePasswordAPIView.as_view(), name='change_password'),
]