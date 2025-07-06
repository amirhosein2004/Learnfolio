import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers


class IdentityValidationMixin:
    def validate_identity(self, value):
        """
        Validates if the input is a valid email or Iranian phone number.
        Returns the cleaned value or raises a validation error.
        """
        value = value.strip()

        # --- Try email validation
        if '@' in value:
            try:
                validate_email(value)
                return value.lower()
            except DjangoValidationError:
                raise serializers.ValidationError(
                    " ایمیل نامعتبر است. لطفاً یک ایمیل معتبر مانند example@example.com وارد کنید"
                )

        # --- Try phone validation
        phone = self.normalize_phone(value)
        if phone and self.is_valid_iranian_phone(phone):
            return phone

        # --- Neither valid email nor phone
        raise serializers.ValidationError(
            "ورودی نامعتبر است. لطفاً یک ایمیل یا شماره تلفن معتبر وارد کنید"
        )

    def normalize_phone(self, phone):
        """
        Normalizes Iranian phone numbers to 09xxxxxxxxx format.
        Supports: +98912..., 0098912..., 98912..., etc.
        """
        phone = re.sub(r'\s+', '', phone)
        phone = phone.replace('+98', '0')
        phone = phone.replace('0098', '0')
        phone = phone.replace('98', '0') if phone.startswith('98') else phone
        return phone

    def is_valid_iranian_phone(self, phone):
        """
        Checks if the phone number is in valid Iranian mobile format.
        Example: 09123456789
        """
        return re.match(r'^09\d{9}$', phone)
