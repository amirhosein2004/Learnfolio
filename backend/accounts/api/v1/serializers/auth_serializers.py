from typing import Any
from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.api.v1.serializers.base_serializers import (
    BaseIdentitySerializer,
    BaseEmailConfirmationLinkSerializer,
    BaseOTPVerificationSerializer
)
from accounts.services.validation_services import (
    get_valid_otp,
    validate_user_with_password,
)
from accounts.services.validation_services import get_identity_purpose

User = get_user_model()

class IdentitySerializer(BaseIdentitySerializer):
    """
    Serializer to validate a user's identity (email or phone number).
    """
    pass

class AuthenticateOTPVerificationSerializer(BaseOTPVerificationSerializer):
    """
    Serializer for verifying an OTP code and identity.
    Requires identity and code.
    """

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """
        Validate the OTP code for the given identity.
        Checks if the OTP exists, is valid, and not expired.
        """
        identity = attrs['identity']
        code = attrs['otp']
        purpose = get_identity_purpose(identity) # determine purpose 

        valid, error = get_valid_otp(identity, code, purpose) # verify otp for given identity
        if error:
            raise serializers.ValidationError({"otp": error})

        return attrs
    
class RegisterConfirmationLinkSerializer(BaseEmailConfirmationLinkSerializer):
    """
    Serializer for verifying a registration confirmation link.
    Requires identity and token.
    """
    def validate_identity(self, value: str) -> str:
        if User.objects.filter(email__iexact=value).exists():
            # TODO: اینجا هم بررسی کن که این پیام را به کاربر بدهم ایراد امنیتی دارد یا نه
            raise serializers.ValidationError(".این ایمیل قبلاً ثبت شده است")
        return super().validate_identity(value)

class PasswordLoginSerializer(BaseIdentitySerializer):
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