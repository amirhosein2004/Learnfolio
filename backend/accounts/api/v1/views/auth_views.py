import logging

from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView

from drf_spectacular.utils import extend_schema

from accounts.schema_docs.v1 import (
    identity_submit_schema,
    otp_verification_schema,
    link_verification_schema,
    resend_otp_or_link_schema,
    password_login_schema,
)
from accounts.api.v1.serializers.auth_serializers import (
    IdentitySerializer,
    OTPVerificationSerializer,
    EmailConfirmationLinkSerializer,
    PasswordLoginSerializer,
)
from accounts.services.auth_services import (
    handle_identity_submission,
    login_or_register_user,
    generate_tokens_for_user,
)
from accounts.services.cache_services import (
    can_resend,
    set_resend_cooldown,
)

from core.decorators.captcha import captcha_required
from core.permissions import IsNotAuthenticated
from core.throttles.throttles import CustomAnonThrottle, ResendOTPOrLinkThrottle, TokenRefreshAnonThrottle

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
    restrict access authenticated users.
    """
    authentication_classes = []  # No authentication required
    permission_classes = [IsNotAuthenticated] # Prevent authenticated users
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
            message, purpose, next_url = handle_identity_submission(identity)
            set_resend_cooldown(identity, 2 * 60)  # set cache for 2 minutes
            return Response({'detail': message, "next_url": next_url, "purpose": purpose}, status=200)
        except Exception:
            logger.error(f"Error processing identity submission for {identity}", exc_info=True)
            return Response({'detail': ".خطای ناشناخته‌ای رخ داده است لطفا دوباره تلاش کنید"}, status=500)       

@extend_schema(**otp_verification_schema)
class OTPOrVerificationAPIView(APIView):
    """
    Verifies OTP codes for login and registration.
    
    Accepts:
    - `identity`: Email or phone number
    - `otp`: 6 digit number
    - `cf-turnstile-response`: CAPTCHA token (ia enable)

    Protected with: CAPTCHA (Cloudflare Turnstile) and 
    Rate-limited via CustomAnonThrottle(return 429 Too Many Requests).
    restrict access authenticated users.
    """
    authentication_classes = []  # No authentication required
    permission_classes = [IsNotAuthenticated]
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

        try:
            user, action, message = login_or_register_user(identity=identity)
            jwt_tokens = generate_tokens_for_user(user)  # create JWT tokens(login)
            logger.info(f"User authenticated: {user.id}")
            return Response({
                'detail': message,
                'action': action,
                'access': jwt_tokens['access'],
                'refresh': jwt_tokens['refresh'],
            }, status=200)
        except Exception:
            logger.error(f"Error processing OTP or link verification for {identity}", exc_info=True)
            return Response({'detail': 'خطای ناشناخته‌ای رخ داده است لطفا دوباره تلاش کنید'}, status=500)

@extend_schema(**link_verification_schema)
class LinkVerificationAPIView(APIView):
    """
    Verifies Confirm links for registration.

    Accepts:
    - `identity`: Email or phone number
    - `token`: token from link
    - `cf-turnstile-response`: CAPTCHA token (ia enable)

    Protected with: CAPTCHA (Cloudflare Turnstile) and 
    Rate-limited via CustomAnonThrottle(return 429 Too Many Requests).
    restrict access authenticated users.
    """
    authentication_classes = []  # No authentication required
    permission_classes = [IsNotAuthenticated]
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
            user, action, message = login_or_register_user(identity=identity)
            jwt_tokens = generate_tokens_for_user(user)  # create JWT tokens(login)
            logger.info(f"User authenticated: {user.id}")
            return Response({
                'detail': message,
                'action': action,
                'access': jwt_tokens['access'],
                'refresh': jwt_tokens['refresh'],
            }, status=200)
        except Exception:
            logger.error(f"Error processing OTP or link verification for {identity}", exc_info=True)
            return Response({'detail': 'خطای ناشناخته‌ای رخ داده است لطفا دوباره تلاش کنید'}, status=500)

@extend_schema(**resend_otp_or_link_schema)
class ResendOTPOrLinkAPIView(APIView):
    """
    Resends a verification OTP or confirmation link to the given identity.
    Validates the identity & Checks cooldown if allowe resend

    Accepts:
    - `identity`: Email or phone number
    - `cf-turnstile-response`: CAPTCHA token (if enabled)

    Protected with: CAPTCHA (Cloudflare Turnstile) and 
    Rate-limited via ResendOTPOrLinkThrottle (returns 429 on cooldown)
    restrict access authenticated users.
    """
    authentication_classes = []  # No authentication required
    permission_classes = [IsNotAuthenticated]
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
            message, purpose, next_url = handle_identity_submission(identity)
            set_resend_cooldown(identity, 2 * 60)  # set cache for 2 minutes
            logger.info(f"resending for {identity}")
            return Response({'detail': message, "next_url": next_url, "purpose": purpose}, status=200)
        except Exception:
            logger.error(f"Error resending for {identity}", exc_info=True)
            return Response({'detail': ".خطای ناشناخته‌ای رخ داده است لطفا دوباره تلاش کنید"}, status=500)

@extend_schema(**password_login_schema)
class PasswordLoginAPIView(APIView):
    """
    validate password for user and login user
    
    Accepts:
    - `identity`: Email or phone number
    - `password`: user password
    - `cf-turnstile-response`: CAPTCHA token (if enabled)

    Protected with: CAPTCHA (Cloudflare Turnstile) and 
    Rate-limited via ResendOTPOrLinkThrottle (returns 429 on cooldown)
    restrict access authenticated users.
    """
    authentication_classes = []  # No authentication required
    permission_classes = [IsNotAuthenticated]
    throttle_classes = [CustomAnonThrottle]

    @captcha_required
    def post(self, request):
        """
        Handles password login for users.
        """
        serializer = PasswordLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        identity = serializer.validated_data['identity']
        user = serializer.validated_data['user']

        try:
            jwt_tokens = generate_tokens_for_user(user)  # create JWT tokens(login)
            logger.info(f"User authenticated with password: {user.id}")
            return Response({
                'detail': "کاربر با موفقیت وارد شد",
                'access': jwt_tokens['access'],
                'refresh': jwt_tokens['refresh'],
            }, status=200)
        except Exception:
            logger.error(f"Error processing logging with password for identityt {identity}", exc_info=True)
            return Response({'detail': 'خطای ناشناخته‌ای رخ داده است لطفا دوباره تلاش کنید'}, status=500)

@extend_schema(summary="دریافت توکن دسترسی و رفرش توکن جدید" ,tags=['auth'])        
class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom Token Refresh View to handle token refresh requests.
    Inherits from SimpleJWT's TokenRefreshView.
    """
    throttle_classes = [TokenRefreshAnonThrottle]  # Prevent abuse by limiting request rate