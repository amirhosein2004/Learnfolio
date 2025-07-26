import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import IdentitySerializer, OTPVerificationSerializer, EmailConfirmationLinkSerializer
from accounts.services.auth_services import (
    handle_identity_submission, 
    handle_otp_verification ,
    handle_link_verification, 
    generate_tokens_for_user,
)
from accounts.services.serializer_services import (
    can_resend, 
    set_resend_cooldown,
)
from drf_spectacular.utils import extend_schema
from accounts.schema_docs.auth_docs import identity_submit_schema
from core.throttles.throttles import CustomAnonThrottle, ResendOTPOrLinkThrottle
from core.decorators.captcha import captcha_required
from django.contrib.auth import get_user_model

User = get_user_model()

logger = logging.getLogger(__name__)

@extend_schema(**identity_submit_schema)
class IdentitySubmissionAPIView(APIView):
    """
    Handles identity submission (email or phone) and sends an OTP or confirmation link.

    Accepts:
    - `identity`: Email or phone number
    - `cf-turnstile-response`: CAPTCHA token (ia enable)
    
    Protected with: CAPTCHA (Cloudflare Turnstile) and 
    Rate-limited via CustomAnonThrottle(return 429 Too Many Requests).
    """
    throttle_classes = [CustomAnonThrottle] # Prevent abuse by limiting request rate

    @captcha_required
    def post(self, request):
        """
        POST method to validate submitted identity (email or phone)
        and trigger OTP or confirmation link sending.
        """
        serializer = IdentitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        identity = serializer.validated_data['identity']

        try:
            message, next_url = handle_identity_submission(identity)
            set_resend_cooldown(identity, 3 * 60)  # set cache for 3 minutes
            return Response({'detail': message, "next_url": next_url}, status=200)
        except Exception:
            logger.error(f"Error processing identity submission for {identity}", exc_info=True)
            return Response({'detail': ".خطای ناشناخته‌ای رخ داده است لطفا دوباره تلاش کنید"}, status=500)       

class OTPOrVerificationAPIView(APIView):
    """
    Verifies OTP codes for login and registration.
    
    Accepts:
    - `identity`: Email or phone number
    - `otp`: 6 digit number
    - `cf-turnstile-response`: CAPTCHA token (ia enable)

    Protected with: CAPTCHA (Cloudflare Turnstile) and 
    Rate-limited via CustomAnonThrottle(return 429 Too Many Requests).
    """
    throttle_classes = [CustomAnonThrottle]  # Prevent abuse by limiting request rate

    @captcha_required
    def post(self, request):
        """
        Handles OTP verification.
        Verifies CAPTCHA, validates OTP, authenticates the user.
        """

        serializer = OTPVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        identity = serializer.validated_data['identity']
        otp = serializer.validated_data['otp']

        try:
            user, action, message = handle_otp_verification(identity=identity, otp_obj=otp)
            tokens = generate_tokens_for_user(user)  # create JWT tokens(login)
            logger.info(f"User authenticated: {user.id}")
            return Response({
                'detail': message,
                'action': action,
                'access': tokens['access'],
                'refresh': tokens['refresh'],
            }, status=200)
        except Exception:
            logger.error(f"Error processing OTP or link verification for", exc_info=True)
            return Response({'detail': 'خطای ناشناخته‌ای رخ داده است لطفا دوباره تلاش کنید'}, status=500)

class LinkVerificationAPIView(APIView):
    """
    Verifies Confirm links for registration.

    Accepts:
    - `identity`: Email or phone number
    - `token`: token from link
    - `cf-turnstile-response`: CAPTCHA token (ia enable)

    Protected with: CAPTCHA (Cloudflare Turnstile) and 
    Rate-limited via CustomAnonThrottle(return 429 Too Many Requests).
    """
    throttle_classes = [CustomAnonThrottle]  # Prevent abuse by limiting request rate
    
    @captcha_required
    def post(self, request):
        """
        Handles confirm link verification.
        Verifies CAPTCHA, validates token, authenticates the user.
        """
        serializer = EmailConfirmationLinkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        identity = serializer.validated_data['identity']

        try:
            user, action, message = handle_link_verification(identity=identity)
            tokens = generate_tokens_for_user(user)  # create JWT tokens(login)
            logger.info(f"User authenticated: {user.id}")
            return Response({
                'detail': message,
                'action': action,
                'access': tokens['access'],
                'refresh': tokens['refresh'],
            }, status=200)
        except Exception:
            logger.error(f"Error processing OTP or link verification for", exc_info=True)
            return Response({'detail': 'خطای ناشناخته‌ای رخ داده است لطفا دوباره تلاش کنید'}, status=500)


class ResendOTPOrLinkAPIView(APIView):
    """
    Resends a verification OTP or confirmation link to the given identity.
    Validates the identity & Checks cooldown if allowe resend

    Accepts:
    - `identity`: Email or phone number
    - `cf-turnstile-response`: CAPTCHA token (if enabled)

    Protected with: CAPTCHA (Cloudflare Turnstile) and 
    Rate-limited via ResendOTPOrLinkThrottle (returns 429 on cooldown)
    """
    throttle_classes = [ResendOTPOrLinkThrottle]

    @captcha_required
    def post(self, request):
        """
        Handles resend requests for OTP or confirmation link.

        if can send: Resends OTP or link using `handle_identity_submission`
        """
        serializer = IdentitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        identity = serializer.validated_data['identity']

        can_send, seconds_left = can_resend(identity)
        if not can_send:
            return Response(
                {
                    "detail": f".لطفا {seconds_left // 60} دقیقه و {seconds_left % 60} ثانیه دیگر برای ارسال مجدد صبر کنید",
                    "cooldown_seconds": seconds_left
                },
                status=429
            )
        try:
            message, next_url = handle_identity_submission(identity)
            set_resend_cooldown(identity, 3 * 60)  # set cache for 3 minutes
            logger.info(f"resending for {identity}")
            return Response({'detail': message, "next_url": next_url}, status=200)
        except Exception:
            logger.error(f"Error resending for {identity}", exc_info=True)
            return Response({'detail': ".خطای ناشناخته‌ای رخ داده است لطفا دوباره تلاش کنید"}, status=500)