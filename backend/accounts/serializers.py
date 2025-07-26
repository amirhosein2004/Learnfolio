from rest_framework import serializers
from accounts.mixins import IdentityValidationMixin
from accounts.services.serializer_services import get_valid_otp, verify_email_link
from django.contrib.auth import get_user_model

User = get_user_model()

class IdentitySerializer(serializers.Serializer, IdentityValidationMixin):
    """
    Serializer to validate a user's identity (email or phone number).
    Often used as the first step before sending an OTP.
    """
    identity = serializers.CharField(required=True, allow_blank=False,
        error_messages={
            'blank': ".لطفاً ایمیل یا شماره تلفن را وارد کنید",
            'required': ".وارد کردن ایمیل یا شماره تلفن الزامی است"
        }
    )

    def validate_identity(self, value):
        # Uses IdentityValidationMixin to normalize and validate the identity.
        return super().validate_identity(value)

class OTPVerificationSerializer(serializers.Serializer, IdentityValidationMixin):
    """
    Serializer for verifying an OTP code and identity.
    Requires identity and code.
    """
    identity = serializers.CharField(
        required=True, allow_blank=False,
        error_messages={
            'blank': ".لطفاً ایمیل یا شماره تلفن را وارد کنید",
            'required': ".وارد کردن ایمیل یا شماره تلفن الزامی است"
        }
    )
    otp = serializers.CharField(
        required=True, allow_blank=False, min_length=6, max_length=6,
        error_messages={
            'blank': ".کد تایید نمی‌تواند خالی باشد",
            'required': ".کد تایید الزامی است",
            'min_length': ".کد تایید باید 6 رقم باشد",
            'max_length': ".کد تایید باید 6 رقم باشد"
        }
    )

    def validate_identity(self, value):
        # Normalize and validate identity (email or phone).
        return super().validate_identity(value)
    
    def validate_otp(self, value):
        if not value.isdigit():
            raise serializers.ValidationError(".کد تأیید باید فقط شامل ارقام باشد")
        return value

    def validate(self, attrs):
        """
        Validate the OTP code for the given identity.
        Checks if the OTP exists, is valid, and not expired.
        """
        identity = attrs['identity']
        code = attrs['otp']

        otp, error = get_valid_otp(identity, code) # verify otp for given identity
        if error:
            raise serializers.ValidationError({"otp": error})

        attrs['otp'] = otp
        return attrs
    
class EmailConfirmationLinkSerializer(serializers.Serializer, IdentityValidationMixin):
    """
    Serializer for verifying an email confirmation link.
    Requires identity and token.
    """
    identity = serializers.CharField(
        required=True, allow_blank=False,
        error_messages={
            'blank': ".لطفاً ایمیل یا شماره تلفن را وارد کنید",
            'required': ".وارد کردن ایمیل یا شماره تلفن الزامی است"
        }
    )
    token = serializers.CharField(
        required=True, allow_blank=False,
        error_messages={
            'required': ".توکن تایید لینک الزامی است",
            'blank': ".توکن تایید لینک نمی‌تواند خالی باشد"
        }
    )

    def validate_identity(self, value):
        # Normalize and validate identity (email or phone).
        return super().validate_identity(value)

    def validate(self, attrs):
        """
        Validate the email confirmation link.
        Checks if the token is valid and not expired.
        """
        token = attrs['token']

        valid, error = verify_email_link(token)

        if error:
            raise serializers.ValidationError({"token": error})

        return attrs

class PasswordLoginSerializer(serializers.Serializer, IdentityValidationMixin):
    """
    Serializer for logging in with identity (email or phone) and password.
    """
    identity = serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=6)

    def validate_identity(self, value):
        # Normalize and validate identity.
        return super().validate_identity(value)

    def validate(self, attrs):
        """
        Authenticate the user using email/phone and password.
        Check if the user exists, the password is correct, and the account is active.
        """
        identity = attrs['identity']
        password = attrs['password']

        # Try to fetch user by email or phone
        if '@' in identity:
            user = User.objects.filter(email__iexact=identity).first()
        else:
            user = User.objects.filter(phone_number=identity).first()

        if not user or not user.check_password(password):
            raise serializers.ValidationError({"detail": " کاربر موجود نیست  یا رمز عبور اشتباه است"})

        if not user.is_active:
            raise serializers.ValidationError({"detail": "حساب کاربری غیرفعال است. لطفاً با پشتیبانی تماس بگیرید"})

        attrs['user'] = user
        return attrs