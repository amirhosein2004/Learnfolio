from rest_framework import serializers
from django.contrib.auth import get_user_model

from accounts.models import AdminProfile
from accounts.api.v1.serializers.base_serializers import (
    BaseIdentitySerializer,
    BaseEmailConfirmationLinkSerializer,
    BaseOTPVerificationSerializer
)
from accounts.mixins import UniqueIdentityValidationMixin, SocialNetworksValidationMixin
from accounts.services.validation_services import get_identity_purpose, get_valid_otp


User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying user profile data.
    """
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone_number']

    def to_representation(self, instance):
        # convert none values to ""
        data = super().to_representation(instance)
        for key, value in data.items():
            if value is None:
                data[key] = ""
        return data


class UserFullNameSerializer(serializers.ModelSerializer):
    """
    Serializer for user's name.
    """
    class Meta:
        model = User
        fields = ['full_name']
        extra_kwargs = {
            'full_name': {
                'required': True,
                'allow_blank': False,
                'min_length': 2,
                'max_length': 100,
                'error_messages': {
                    'blank': '.نام و نام خانوادگی نمی تواند خالی باشد',
                    'required': '.نام و نام خانوادگی الزامی است',
                    'min_length': '.نام و نام خانوادگی باید حداقل 2 حرف باشد',
                    'max_length': '.نام و نام خانوادگی باید حداکثر 100 حرف باشد'
                }
            }
        }

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.save()
        return instance


class AdminProfileSerializer(serializers.ModelSerializer, SocialNetworksValidationMixin):
    """
    Serializer for admin profile.
    """
    class Meta:
        model = AdminProfile
        fields = ['social_networks', 'description']
        extra_kwargs = {
            'description': {
                'required': False,
                'allow_blank': True,
                'max_length': 1000,
                'error_messages': {
                    'max_length': '.توضیحات باید حداکثر 1000 حرف باشد'
                }
            },
            'social_networks': {
                'required': False,
                'allow_null': True,
                'error_messages': {
                    'invalid': '.فرمت شبکه‌های اجتماعی معتبر نیست'
                }
            }
        }


    def update(self, instance, validated_data):
        instance.social_networks = validated_data.get('social_networks', instance.social_networks)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class UserPhoneOrEmailUpdateSerilizer(BaseIdentitySerializer, UniqueIdentityValidationMixin):
    """
    Serializer for updating user's phone or email.
    """
    
    pass
    

class VerifyOTPUserPhoneUpdateSerilizer(BaseOTPVerificationSerializer, UniqueIdentityValidationMixin):
    """
    Serializer for verifying OTP for updating user's phone.
    """
    
    def validate(self, attrs):
        """
        Validate the OTP code for the given identity.
        Checks if the OTP exists, is valid, and not expired.
        """
        identity = attrs['identity']
        code = attrs['otp']
        purpose = get_identity_purpose(identity, context="update_identity") # determine purpose 

        valid, error = get_valid_otp(identity, code, purpose) # verify otp for given identity
        if error:
            raise serializers.ValidationError({"otp": error})

        return attrs

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get('identity', instance.phone_number)
        instance.save()
        return instance


class ConfirmationLinkEmailUpdateSerializer(BaseEmailConfirmationLinkSerializer, UniqueIdentityValidationMixin):
    """
    Serializer for validating updating email with a confirmation link.
    """

    def update(self, instance, validated_data):
        instance.email = validated_data.get('identity', instance.email)
        instance.save()
        return instance
