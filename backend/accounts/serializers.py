from rest_framework import serializers
from .mixins import IdentityValidationMixin
from .models import OTP
from django.contrib.auth import get_user_model

User = get_user_model()

class IdentitySerializer(serializers.Serializer, IdentityValidationMixin):
    """
    Serializer to validate a user's identity (email or phone number).
    Often used as the first step before sending an OTP.
    """
    identity = serializers.CharField()

    def validate_identity(self, value):
        # Uses IdentityValidationMixin to normalize and validate the identity.
        return super().validate_identity(value)

class OTPVerificationSerializer(serializers.Serializer, IdentityValidationMixin):
    """
    Serializer for verifying an OTP code for a given purpose (login, register, or reset).
    Requires identity, code, and purpose.
    """
    identity = serializers.CharField()
    code = serializers.CharField(min_length=6, max_length=6)
    purpose = serializers.ChoiceField(choices=['login', 'register', 'reset'])

    def validate_identity(self, value):
        # Normalize and validate identity (email or phone).
        return super().validate_identity(value)

    def validate(self, attrs):
        """
        Check that an OTP exists for the provided identity, code, and purpose.
        Ensure it hasn't expired.
        """
        identity = attrs['identity']
        code = attrs['code']
        purpose = attrs['purpose']

        filters = {'code': code, 'purpose': purpose}
        if '@' in identity:
            filters['email'] = identity
        else:
            filters['phone_number'] = identity

        try:
            otp = OTP.objects.get(**filters)    
        except OTP.DoesNotExist:
            raise serializers.ValidationError({"code": "کد وارد شده برای این عملیات نامعتبر یا منقضی شده است"})

        if otp.is_expired():
            raise serializers.ValidationError({"code": "کد منقضی شده است. لطفاً دوباره درخواست ارسال کد بدهید"})

        attrs['otp'] = otp
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