import logging

from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema
from accounts.schema_docs.v1 import (
    request_password_reset_schema,
    otp_verification_password_reset_schema,
    link_verification_password_reset_schema,
    reset_password_schema,
    first_time_password_schema,
    change_password_schema
)

from accounts.api.v1.serializers.auth_serializers import IdentitySerializer
from accounts.api.v1.serializers.password_serializers import (
    ResetOTPVerificationSerializer,
    ResetPasswordConfirmationLinkSerializer,
    SetResetPasswordSerializer,
    SetFirstTimePasswordSerializer,
    ChangePasswordSerializer
)
from accounts.services.password_services import (
    handle_password_reset,
    generate_reset_password_token,
    change_user_password,
)
from core.decorators.captcha import captcha_required
from core.permissions import (
    UserIsNotAuthenticated, UserIsAuthenticated,
    HasNoPassword, HasPassword
)
from core.throttles.throttles import (
    CustomAnonThrottle,
    CustomUserThrottle
)
from accounts.services.cache_services import set_resend_cooldown

User = get_user_model()

logger = logging.getLogger(__name__)


@extend_schema(**request_password_reset_schema)
class RequestPasswordResetAPIView(APIView):
    """
    Request password reset for a user by email or phone number.

    Accepts:
    - `identity`: Email or phone number
    - `cf-turnstile-response`: CAPTCHA token (ia enable)
    
    Protected with: CAPTCHA (Cloudflare Turnstile) and 
    Rate-limited via CustomAnonThrottle(return 429 Too Many Requests).
    restrict access authenticated users.
    """
    authentication_classes = []
    permission_classes = [UserIsNotAuthenticated]
    throttle_classes = [CustomAnonThrottle]

    @captcha_required
    def post(self, request, *args, **kwargs):
        serializer = IdentitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        identity = serializer.validated_data['identity']

        try:
            message, purpose, next_url = handle_password_reset(identity)
            set_resend_cooldown(identity, purpose=purpose, timeout=2 * 60)
            return Response({'detail': message, "next_url": next_url, "purpose": purpose}, status=200)
        except Exception:
            logger.error(f"Error processing for request password reset for {identity}", exc_info=True)
            return Response({'detail': ".خطای ناشناخته‌ای رخ داده است لطفا دوباره تلاش کنید"}, status=500)


@extend_schema(**otp_verification_password_reset_schema)
class OTPVerificationPasswordResetAPIView(APIView):
    """
    Verify OTP for password reset.

    Accepts:
    - `identity`: phone number
    - `otp`: 6 digit number
    - `cf-turnstile-response`: CAPTCHA token (ia enable)
    
    Protected with: CAPTCHA (Cloudflare Turnstile) and 
    Rate-limited via CustomAnonThrottle(return 429 Too Many Requests).
    restrict access authenticated users.
    """
    authentication_classes = []
    permission_classes = [UserIsNotAuthenticated]
    throttle_classes = [CustomAnonThrottle]

    @captcha_required
    def post(self, request, *args, **kwargs):
        serializer = ResetOTPVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            reset_token = generate_reset_password_token(serializer.validated_data['identity'])
            return Response({"detail": "کد تایید شد", "reset_token": reset_token})
        except Exception:
            logger.error(f"Error processing OTP verification for password reset for {serializer.validated_data['identity']}", exc_info=True)
            return Response({'detail': ".خطای ناشناخته‌ای رخ داده است لطفا دوباره تلاش کنید"}, status=500)


@extend_schema(**link_verification_password_reset_schema)
class LinkVerificationPasswordResetAPIView(APIView):
    """
    Verify confirmation link for password reset.

    Accepts:
    - `identity`: Email
    - `token`: token from link
    - `cf-turnstile-response`: CAPTCHA token (ia enable)
    
    Protected with: CAPTCHA (Cloudflare Turnstile) and 
    Rate-limited via CustomAnonThrottle(return 429 Too Many Requests).
    restrict access authenticated users.
    """
    authentication_classes = []
    permission_classes = [UserIsNotAuthenticated]
    throttle_classes = [CustomAnonThrottle]

    @captcha_required
    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordConfirmationLinkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            reset_token = generate_reset_password_token(serializer.validated_data['identity'])
            return Response({"detail": "لینک تایید شد", "reset_token": reset_token})
        except Exception:
            logger.error(f"Error processing link verification for password reset for {serializer.validated_data['identity']}", exc_info=True)
            return Response({'detail': ".خطای ناشناخته‌ای رخ داده است لطفا دوباره تلاش کنید"}, status=500)


@extend_schema(**reset_password_schema)
class ResetPasswordAPIView(APIView):
    """
    Reset password for a user by email or phone number.
    
    Accepts:
    - `reset_token`: token from link
    - `new_password`: new password
    - `confirm_password`: confirm password
    - `cf-turnstile-response`: CAPTCHA token (ia enable)
    
    Protected with: CAPTCHA (Cloudflare Turnstile) and 
    Rate-limited via CustomAnonThrottle(return 429 Too Many Requests).
    restrict access authenticated users.
    """
    authentication_classes = []
    permission_classes = [UserIsNotAuthenticated]
    throttle_classes = [CustomAnonThrottle]

    @captcha_required
    def post(self, request, *args, **kwargs):
        serializer = SetResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            change_user_password(serializer.context['user'], serializer.validated_data['new_password'])
            return Response({"detail": ".رمز عبور تغییر یافت"})
        except Exception:
            logger.error(f"Error processing reset password for {serializer.context['identity']}", exc_info=True)
            return Response({'detail': ".خطای ناشناخته‌ای رخ داده است لطفا دوباره تلاش کنید"}, status=500)


@extend_schema(**first_time_password_schema)
class FirstTimePasswordAPIView(APIView):
    """
    Set password for the first time.
    
    Accepts:
    - `new_password`: new password
    - `confirm_password`: confirm password
    
    Rate-limited via CustomUserThrottle(return 429 Too Many Requests).
    restrict access unauthenticated users.
    """
    permission_classes = [UserIsAuthenticated, HasNoPassword]  
    throttle_classes = [CustomUserThrottle]

    def post(self, request, *args, **kwargs):
        serializer = SetFirstTimePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            change_user_password(request.user, serializer.validated_data['new_password'])
            return Response({"detail": "رمز عبور تغییر یافت"})
        except Exception:
            logger.error(f"Error processing first time password for {request.user.id}", exc_info=True)
            return Response({'detail': ".خطای ناشناخته‌ای رخ داده است لطفا دوباره تلاش کنید"}, status=500)


@extend_schema(**change_password_schema)
class ChangePasswordAPIView(APIView):
    """
    Change password for a user.
    
    Accepts:
    - `old_password`: old password
    - `new_password`: new password
    - `confirm_password`: confirm password
    
    Rate-limited via CustomUserThrottle(return 429 Too Many Requests).
    restrict access unauthenticated users.
    """
    permission_classes = [UserIsAuthenticated, HasPassword]  
    throttle_classes = [CustomUserThrottle] 

    def patch(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)

        try:
            change_user_password(request.user, serializer.validated_data['new_password'])
            return Response({"detail": ".رمز عبور تغییر یافت"})
        except Exception:
            logger.error(f"Error processing change password for {request.user.id}", exc_info=True)
            return Response({'detail': ".خطای ناشناخته‌ای رخ داده است لطفا دوباره تلاش کنید"}, status=500)
