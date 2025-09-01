from typing import Any
from rest_framework import serializers
from accounts.api.v1.serializers.base_serializers import (
    BaseEmailConfirmationLinkSerializer,
    BaseOTPVerificationSerializer,
    BaseSetPasswordSerializer
)
from accounts.mixins import CaptchaSerializerMixin
from accounts.services.validation_services import get_identity_purpose, get_valid_otp
from django.contrib.auth import get_user_model
from accounts.services.password_services import get_user_by_identity
from accounts.services.validation_services import validate_reset_password_token

User = get_user_model()

class ResetPasswordConfirmationLinkSerializer(BaseEmailConfirmationLinkSerializer, CaptchaSerializerMixin):
    """
    Serializer for validating resetting password with a confirmation link.
    """
    pass

class ResetOTPVerificationSerializer(BaseOTPVerificationSerializer, CaptchaSerializerMixin):
    """
    Serializer for verifying an OTP code and identity.
    Requires identity and code.
    """

    def validate(self, attrs):
        """
        Validate the OTP code for the given identity.
        Checks if the OTP exists, is valid, and not expired.
        """
        identity = attrs['identity']
        code = attrs['otp']
        purpose = get_identity_purpose(identity, context="reset_password") # determine purpose 

        valid, error = get_valid_otp(identity, code, purpose) # verify otp for given identity
        if error:
            raise serializers.ValidationError({"otp": error})

        return attrs

class SetResetPasswordSerializer(BaseSetPasswordSerializer, CaptchaSerializerMixin):
    """
    Serializer for setting a new password after reset.
    """
    reset_token = serializers.CharField(
        required=True,
        error_messages={
            'blank': '.توکن ریست پسورد خالی است',
            'required': '.توکن ریست پسورد الزامی است',
        }
    )

    def validate_reset_token(self, value: str) -> str:
        """
        Validate reset token and resolve user.
        """
        try:
            raw_token = validate_reset_password_token(value)
        except Exception:
            raise serializers.ValidationError("شما نمی‌توانید این کار را انجام دهید، لطفا دوباره امتحان کنید")

        # resolve user
        identity = raw_token.get("identity")
        user = get_user_by_identity(identity)

        # save user for use in view
        self.context["user"] = user
        self.context["identity"] = identity
        return value

class SetFirstTimePasswordSerializer(BaseSetPasswordSerializer):
    """
    Serializer for setting a first time password.
    """

class ChangePasswordSerializer(BaseSetPasswordSerializer):
    """
    Serializer for changing a user's password.
    """
    old_password = serializers.CharField(
        required=True,
        error_messages={
            'blank': '.رمز عبور فعلی خالی است',
            'required': '.رمز عبور فعلی الزامی است',
        }
    )

    def validate_old_password(self, value):
        user = self.context.get('user')
        if not user.check_password(value):
            raise serializers.ValidationError('.رمز عبور فعلی اشتباه است')
        return value

    def validate(self, data):
        validated_data = super().validate(data)
        if validated_data["old_password"] == validated_data["new_password"]:
            raise serializers.ValidationError({'detail': '.رمز فعلی و جدید نمیتوانند یکسان باشند'})
        return validated_data