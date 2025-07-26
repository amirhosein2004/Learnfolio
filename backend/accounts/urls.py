from django.urls import path
from .views.auth_views import IdentitySubmissionAPIView, OTPOrVerificationAPIView, ResendOTPOrLinkAPIView, LinkVerificationAPIView

app_name = 'accounts'

urlpatterns = [
    path('submit-identity/', IdentitySubmissionAPIView.as_view(), name='submit_identity'),
    path('verify-otp/', OTPOrVerificationAPIView.as_view(), name='verify_otp'),
    path('verify-link/', LinkVerificationAPIView.as_view(), name='verify_link'),
    path('resend-otp-or-link/', ResendOTPOrLinkAPIView.as_view(), name='resend_otp_or_link')
]