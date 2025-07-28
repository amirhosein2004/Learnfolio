from rest_framework import serializers
from accounts.mixins import IdentityValidationMixin

# common base class
class BaseIdentitySerializer(serializers.Serializer, IdentityValidationMixin):
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