import logging

from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.exceptions import ValidationError

from drf_spectacular.utils import extend_schema

from accounts.schema_docs.v1 import (
    identity_submit_schema,
    otp_verification_schema,
    link_verification_schema,
    password_login_schema,
    logout_schema
)
from accounts.api.v1.serializers.auth_serializers import (
    IdentitySerializer,
    AuthenticateOTPVerificationSerializer,
    RegisterConfirmationLinkSerializer,
    PasswordLoginSerializer,
)
from accounts.services.auth_services import (
    handle_identity_submission,
    login_or_register_user,
    generate_tokens_for_user,
    logout_user
)
from accounts.services.validation_services import get_identity_purpose
from accounts.services.cache_services import (
    can_resend,
    set_resend_cooldown,
)

from core.decorators.captcha import captcha_required
from core.permissions import UserIsNotAuthenticated, UserIsAuthenticated
from core.throttles.throttles import (
    CustomAnonThrottle,
    TokenRefreshUserThrottle
)


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
    permission_classes = [UserIsNotAuthenticated] # Prevent authenticated users
    throttle_classes = [CustomAnonThrottle] # Prevent abuse by limiting request rate

    @captcha_required
    def post(self, request):
        serializer = IdentitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        identity = serializer.validated_data['identity']

        # Determine purpose first without sending anything
        purpose = get_identity_purpose(identity)
        
        # Check cooldown with the correct purpose
        can_send, seconds_left = can_resend(identity, purpose)
        if not can_send:
            return Response(
                {
                    "detail": f"لطفا {seconds_left // 60} دقیقه و {seconds_left % 60} ثانیه دیگر برای ارسال مجدد صبر کنید",
                    "cooldown_seconds": seconds_left
                },
                status=429
            )

        try:
            message, purpose, next_url = handle_identity_submission(identity)
            set_resend_cooldown(identity, purpose=purpose, timeout=2 * 60)
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
    permission_classes = [UserIsNotAuthenticated]
    throttle_classes = [CustomAnonThrottle]  # Prevent abuse by limiting request rate

    @captcha_required
    def post(self, request):
        serializer = AuthenticateOTPVerificationSerializer(data=request.data)
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
    permission_classes = [UserIsNotAuthenticated]
    throttle_classes = [CustomAnonThrottle]  # Prevent abuse by limiting request rate
    
    @captcha_required
    def post(self, request):
        serializer = RegisterConfirmationLinkSerializer(data=request.data)
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


@extend_schema(**password_login_schema)
class PasswordLoginAPIView(APIView):
    """
    validate password for user and login user
    
    Accepts:
    - `identity`: Email or phone number
    - `password`: user password
    - `cf-turnstile-response`: CAPTCHA token (if enabled)

    Protected with: CAPTCHA (Cloudflare Turnstile) and 
    Rate-limited via CustomAnonThrottle (returns 429 Too Many Requests).
    restrict access authenticated users.
    """
    authentication_classes = []  # No authentication required
    permission_classes = [UserIsNotAuthenticated]
    throttle_classes = [CustomAnonThrottle]

    @captcha_required
    def post(self, request):
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
        

@extend_schema(**logout_schema)
class LogoutAPIView(APIView):
    """
    Handles user logout by invalidating the refresh token.
    """
    permission_classes = [UserIsAuthenticated]  # Only authenticated users can access

    def post(self, request):
        refresh_token = request.data.get('refresh', None)
        
        try:
            logout_user(request.user, refresh_token)
            return Response({'detail': '.با موفقیت خارج شدید'}, status=205)
        except ValidationError as e:
            return Response(e.detail, status=400)
        except Exception:
            logger.error(f"Error during logout for user {request.user.id}", exc_info=True)
            return Response({'detail': '.خطای ناشناخته‌ای رخ داده است لطفا دوباره تلاش کنید'}, status=500)


@extend_schema(summary="دریافت توکن دسترسی و رفرش توکن جدید" ,tags=['auth'])        
class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom Token Refresh View to handle token refresh requests.
    Inherits from SimpleJWT's TokenRefreshView.
    """
    throttle_classes = [TokenRefreshUserThrottle]  # Prevent abuse by limiting request rate
