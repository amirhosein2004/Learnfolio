import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from django.core.validators import URLValidator

class IdentityValidationMixin:
    def validate_identity(self, value):
        """
        Validates if the input is a valid email or Iranian phone number.
        Supports Persian/Arabic digits and normalizes them.
        Returns the cleaned value or raises a validation error.
        """
        value = self.normalize_digits(value.strip()) # normalize digits email or phone

        # --- Try email validation
        if '@' in value:
            try:
                validate_email(value)
                return value.lower()
            except DjangoValidationError:
                raise serializers.ValidationError(
                    "وارد کنید example@example.com ایمیل نامعتبر است. لطفاً یک ایمیل معتبر مانند "
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
    
    def normalize_digits(self, text: str) -> str:
        """
        Converts Persian and Arabic digits in a string to English digits.
        """
        persian_digits = '۰۱۲۳۴۵۶۷۸۹'
        arabic_digits = '٠١٢٣٤٥٦٧٨٩'
        english_digits = '0123456789'

        translation_table = str.maketrans(
            persian_digits + arabic_digits,
            english_digits * 2
        )
        return text.translate(translation_table)

    def is_valid_iranian_phone(self, phone):
        """
        Checks if the phone number is in valid Iranian mobile format.
        Example: 09123456789
        """
        return re.match(r'^09\d{9}$', phone)


class CaptchaSerializerMixin:
    """
    Mixin for serializers that require captcha validation.
    """
    cf_turnstile_response = serializers.CharField(
        required=True,
        allow_blank=False,
        help_text="توکن کپچا که باید از کلاینت ارسال شود"
    )


class UniqueIdentityValidationMixin:
    def validate_identity(self, value: str) -> str:
        is_email = '@' in value
        lookup = {'email__iexact': value} if is_email else {'phone__iexact': value}

        if User.objects.filter(**lookup).exists():
            msg = ".این ایمیل قبلاً ثبت شده است" if is_email else ".این شماره قبلاً ثبت شده است"
            raise serializers.ValidationError(msg)
        
        return value


class SocialNetworksValidationMixin:
    """
    Mixin for validating social network links.
    Ensures the structure is a dict, platforms are allowed, 
    and URLs match the expected format.
    """

    allowed_platforms = [
        "instagram", "telegram", "twitter", "linkedin",
        "youtube", "github", "website", "facebook",
    ]

    def validate_social_networks(self, value):
        """
        Validate social networks data structure and URLs.
        """
        if value is None:
            return value

        if not isinstance(value, dict):
            raise serializers.ValidationError(".شبکه‌های اجتماعی باید به صورت دیکشنری باشد")

        url_validator = URLValidator()

        for platform, url in value.items():
            # --- Check platform is allowed
            if platform not in self.allowed_platforms:
                raise serializers.ValidationError(f".مجاز نیست {platform} پلتفرم")

            # --- Check URL format
            if url and isinstance(url, str):
                try:
                    url_validator(url)
                except DjangoValidationError:
                    raise serializers.ValidationError(f".مجاز نیست {platform} لینک")

                # --- Extra platform-specific checks
                if platform == "instagram" and not re.match(r"https?://(www\.)?instagram\.com/.+", url):
                    raise serializers.ValidationError(f".باشد instagram.com لینک اینستاگرام باید از دامنه")

                elif platform == "telegram" and not re.match(r"https?://(t\.me|telegram\.me)/.+", url):
                    raise serializers.ValidationError(f".باشد t.me یا telegram.me لینک تلگرام باید از دامنه")

                elif platform == "github" and not re.match(r"https?://(www\.)?github\.com/.+", url):
                    raise serializers.ValidationError(f".باشد github.com لینک گیت‌هاب باید از دامنه")

                elif platform == "linkedin" and not re.match(r"https?://(www\.)?linkedin\.com/.+", url):
                    raise serializers.ValidationError(f".باشد linkedin.com لینک لینکدین باید از دامنه")

            elif url is not None and not isinstance(url, str):
                raise serializers.ValidationError(f"لینک {platform} باید رشته متنی باشد")

        return value
