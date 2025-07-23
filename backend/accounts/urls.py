from django.urls import path
from .views.auth_views import IdentitySubmissionAPIView, OTPOrLinkVerificationAPIView

app_name = 'accounts'

urlpatterns = [
    path('submit-identity/', IdentitySubmissionAPIView.as_view(), name='submit_identity'),
    path('verify-otp-or-link/', OTPOrLinkVerificationAPIView.as_view(), name='verify_otp_or_link'),
]