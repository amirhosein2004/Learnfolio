from typing import Any
from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.api.v1.serializers.base_serializers import BaseIdentitySerializer
from accounts.services.validation_services import (
    get_valid_otp,
    validate_user_with_password,
    verify_email_link,
)
from accounts.services.validation_services import get_otp_purpose
from core.serializers import CaptchaSerializer

User = get_user_model()

class IdentitySerializer(BaseIdentitySerializer, CaptchaSerializer):
    """
    Serializer to validate a user's identity (email or phone number).
    """
    pass

class OTPVerificationSerializer(BaseIdentitySerializer, CaptchaSerializer):
    """
    Serializer for verifying an OTP code and identity.
    Requires identity and code.
    """
    otp = serializers.CharField(
        required=True, allow_blank=False, min_length=6, max_length=6,
        error_messages={
            'blank': ".کد تایید نمی‌تواند خالی باشد",
            'required': ".کد تایید الزامی است",
            'min_length': ".کد تایید باید 6 رقم باشد",
            'max_length': ".کد تایید باید 6 رقم باشد"
        }
    )
    
    def validate_otp(self, value: str) -> str:
        if not value.isdigit():
            raise serializers.ValidationError(".کد تأیید باید فقط شامل ارقام باشد")
        return value

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """
        Validate the OTP code for the given identity.
        Checks if the OTP exists, is valid, and not expired.
        """
        identity = attrs['identity']
        code = attrs['otp']
        purpose = get_otp_purpose(identity) # determine purpose 

        valid, error = get_valid_otp(identity, code, purpose) # verify otp for given identity
        if error:
            raise serializers.ValidationError({"otp": error})

        return attrs
    
class EmailConfirmationLinkSerializer(BaseIdentitySerializer, CaptchaSerializer):
    """
    Serializer for verifying an email confirmation link.
    Requires identity and token.
    """
    token = serializers.CharField(
        required=True, allow_blank=False,
        error_messages={
            'required': ".توکن تایید لینک الزامی است",
            'blank': ".توکن تایید لینک نمی‌تواند خالی باشد"
        }
    )

    def validate_identity(self, value: str) -> str:
        if '@' not in value:
            raise serializers.ValidationError(".برای تایید لینک ایمیل، لطفاً یک آدرس ایمیل معتبر وارد کنید")
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(".این ایمیل قبلاً ثبت شده است")
        return super().validate_identity(value)

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """
        Validate the email confirmation link.
        Checks if the token is valid and not expired.
        """
        token = attrs['token']

        valid, error = verify_email_link(token)

        if error:
            raise serializers.ValidationError({"token": error})

        return attrs

class PasswordLoginSerializer(BaseIdentitySerializer, CaptchaSerializer):
    """
    Serializer for logging in with identity (email or phone) and password.
    """
    password = serializers.CharField(
        write_only=True, required=True, allow_blank=False, min_length=8,
        error_messages={
            'required': ".وارد کردن رمز عبور الزامی است",
            'blank': ".رمز عبور نمی‌تواند خالی باشد",
            'min_length': ".رمز عبور باید حداقل ۸ کاراکتر باشد",
        }
    )

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """
        Authenticate the user using email/phone and password.
        Check if the user exists, the password is correct.
        """
        identity = attrs['identity']
        password = attrs['password']

        valid, result = validate_user_with_password(identity, password)
        if not valid:
            raise serializers.ValidationError({"detail": result})

        attrs['user'] = result
        return attrs