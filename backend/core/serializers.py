from rest_framework import serializers

class CaptchaSerializer(serializers.Serializer):
    cf_turnstile_response = serializers.CharField(
        allow_blank=True, required=False,
        help_text="توکن کپچا که باید از کلاینت ارسال شود"
    )