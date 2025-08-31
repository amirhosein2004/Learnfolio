import logging
from rest_framework import status

from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.views import APIView
from urllib3 import request

from drf_spectacular.utils import extend_schema
from accounts.api.v1.serializers.profile_serializers import (
    UserProfileSerializer,
    UserFullNameSerializer,
    AdminProfileSerializer,
    UserPhoneOrEmailUpdateSerilizer,
    VerifyOTPUserPhoneUpdateSerilizer,
    ConfirmationLinkEmailUpdateSerializer
)
from accounts.services.profile_services import handle_identity_update, delete_user_account
from accounts.services.cache_services import set_resend_cooldown
from core.permissions import UserIsAuthenticated, UserAdminIsAuthenticated
from core.throttles.throttles import CustomUserThrottle
from accounts.models import AdminProfile


User = get_user_model()


logger = logging.getLogger(__name__)


class UserProfileAPIView(APIView):
    """
    Profile user
    
    Rate-limited via CustomUserThrottle(return 429 Too Many Requests).
    restrict access unauthenticated users.
    """
    permission_classes = [UserIsAuthenticated]
    throttle_classes = [CustomUserThrottle]

    def get(self, request):
        """
        Get user profile.
        """
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        """
        Update user profile.
        
        Accepts:
        - `full_name`: Full name
        """
        serializer = UserFullNameSerializer(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
            return Response({"detail": ".نام و نام خانوادگی با موفقیت تغییر یافت"})
        except Exception:
            logger.error(f"Error processing user profile update for {request.user.id}", exc_info=True)
            return Response({'detail': ".خطای ناشناخته‌ای رخ داده است لطفا دوباره تلاش کنید"}, status=500)

    def delete(self, request):
        """
        Delete user account.
        """
        try:
            delete_user_account(request.user)            
            return Response({'detail': '.حساب کاربری شما با موفقیت حذف شد'}, status=200)
        except Exception:
            logger.error(f"Error deleting user account for {request.user.id}", exc_info=True)
            return Response({'detail': '.خطای ناشناخته‌ای در حذف حساب کاربری رخ داده است'}, status=500)
        
        
class AdminProfileAPIView(APIView):
    """
    Profile admin user
    
    Rate-limited via CustomUserThrottle(return 429 Too Many Requests).
    restrict access unauthenticated and not admin users.
    """
    permission_classes = [UserAdminIsAuthenticated]
    throttle_classes = [CustomUserThrottle]

    def get(self, request):
        """
        Get admin profile.
        """
        admin_user = AdminProfile.objects.get(user=request.user)
        serializer = AdminProfileSerializer(admin_user)
        return Response(serializer.data)
    
    def patch(self, request):  
        """
        Update admin profile.
        
        Accepts:
        - `social_networks`: Social networks
        - `description`: Description
        """      
        admin_user = AdminProfile.objects.get(user=request.user)
        serializer = AdminProfileSerializer(instance=admin_user, data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
            return Response({"detail": ".پروفایل ادمین با موفقیت به‌روزرسانی شد"})
        except Exception:
            logger.error(f"Error processing admin profile update for {request.user.id}", exc_info=True)
            return Response({'detail': ".خطای ناشناخته‌ای رخ داده است لطفا دوباره تلاش کنید"}, status=500)


class UserUpdateEmailOrPhoneAPIView(APIView):
    """
    Request for update user's email or phone number.
    
    Accepts:
    - `identity`: Email or phone number
    
    Rate-limited via CustomUserThrottle(return 429 Too Many Requests).
    restrict access unauthenticated users.
    """
    permission_classes = [UserIsAuthenticated]
    throttle_classes = [CustomUserThrottle]
    
    def patch(self, request):
        serializer = UserPhoneOrEmailUpdateSerilizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        identity = serializer.validated_data['identity']

        try:
            message, purpose, next_url = handle_identity_update(identity)
            set_resend_cooldown(identity, purpose=purpose, timeout=2 * 60)
            return Response({'detail': message, "next_url": next_url, "purpose": purpose}, status=200)
        except Exception:
            logger.error(f"Error processing user profile update for {request.user.id}", exc_info=True)
            return Response({'detail': ".خطای ناشناخته‌ای رخ داده است لطفا دوباره تلاش کنید"}, status=500)
    

class VerifyOTPUserUpdatePhoneAPIView(APIView):
    """
    Verify OTP for updating user's phone.
    
    Accepts:
    - `identity`: phone number
    - `otp`: 6 digit number
    
    Rate-limited via CustomUserThrottle(return 429 Too Many Requests).
    restrict access unauthenticated users.
    """
    permission_classes = [UserIsAuthenticated]
    throttle_classes = [CustomUserThrottle]
    
    def patch(self, request):
        serializer = VerifyOTPUserPhoneUpdateSerilizer(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
            return Response({'detail': ".شماره تلفن با موفقیت تغیر کرد"}, status=200)
        except Exception:
            logger.error(f"Error processing user profile update for {request.user.id}", exc_info=True)
            return Response({'detail': ".خطای ناشناخته‌ای رخ داده است لطفا دوباره تلاش کنید"}, status=500)


class ConfirmationLinkUserUpdateEmailAPIView(APIView):
    """
    Update user's email with a confirmation link.
    
    Accepts:
    - `identity`: Email
    - `token`: token from link
    
    Rate-limited via CustomUserThrottle(return 429 Too Many Requests).
    restrict access unauthenticated users.
    """
    permission_classes = [UserIsAuthenticated]
    throttle_classes = [CustomUserThrottle]
    
    def patch(self, request):
        serializer = ConfirmationLinkEmailUpdateSerializer(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
            return Response({'detail': ".ایمیل با موفقیت تغیر کرد"}, status=200)
        except Exception:
            logger.error(f"Error processing user profile update for {request.user.id}", exc_info=True)
            return Response({'detail': ".خطای ناشناخته‌ای رخ داده است لطفا دوباره تلاش کنید"}, status=500)
