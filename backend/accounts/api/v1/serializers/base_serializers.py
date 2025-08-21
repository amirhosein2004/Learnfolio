from typing import Any
from rest_framework import serializers
from accounts.mixins import IdentityValidationMixin, CaptchaSerializerMixin
from accounts.services.validation_services import verify_email_link
from django.contrib.auth.password_validation import validate_password

# common base classes
class BaseIdentitySerializer(serializers.Serializer, IdentityValidationMixin, CaptchaSerializerMixin):
    """
    Shared base serializer that includes identity field and validation.
    Should not be used directly in views.
    """
    identity = serializers.CharField(
        required=True, allow_blank=False,
        error_messages={
            'blank': ".لطفاً ایمیل یا شماره تلفن را وارد کنید",
            'required': ".وارد کردن ایمیل یا شماره تلفن الزامی است"
        }
    )

    def validate_identity(self, value: str) -> str:
        return super().validate_identity(value)

class BaseEmailConfirmationLinkSerializer(BaseIdentitySerializer):
    """
    Base serializer for email confirmation link.
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

class BaseOTPVerificationSerializer(BaseIdentitySerializer):
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

class BaseSetPasswordSerializer(serializers.Serializer):
    """
    Serializer for setting a new password.
    """
    new_password = serializers.CharField(
        required=True,
        error_messages={
            'blank': '.رمز عبور جدید خالی است',
            'required': '.رمز عبور جدید الزامی است',
        }
    )
    confirm_password = serializers.CharField(
        required=True,
        error_messages={
            'blank': '.تایید رمز عبور خالی است',
            'required': '.تایید رمز عبور الزامی است',
        }
    )

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({'detail': '.رمزهای عبور مطابقت ندارند'})
        return data
    