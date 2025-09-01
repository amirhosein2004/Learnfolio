from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from accounts.api.v1.serializers.auth_serializers import IdentitySerializer
from accounts.schema_docs.v1.common_schemas import STANDARD_ERROR_RESPONSES

request_password_reset_schema = {
    "request": IdentitySerializer,
    "responses": {
        200: OpenApiResponse(
            description=".درخواست بازیابی رمز عبور با موفقیت ارسال شد",
            response={
                "detail": "پیام موفقیت‌آمیز به فارسی",
                "next_url": "آدرس مرحله بعد",
                "purpose": "reset_password"
            },
            examples=[
                OpenApiExample(
                    name="درخواست بازیابی با ایمیل",
                    value={
                        "detail": ".لینک بازیابی رمز عبور به ایمیل شما ارسال شد",
                        "next_url": "/api/v1/accounts/password/verify-link/",
                        "purpose": "reset_password"
                    },
                    response_only=True,
                ),
                OpenApiExample(
                    name="درخواست بازیابی با شماره موبایل",
                    value={
                        "detail": ".کد بازیابی رمز عبور برای شماره شما ارسال شد",
                        "next_url": "/api/v1/accounts/password/verify-otp/",
                        "purpose": "reset_password"
                    },
                    response_only=True,
                ),
            ]
        ),
        400: OpenApiResponse(
            description=".خطاهای اعتبارسنجی کپچا یا شناسه (ایمیل یا شماره موبایل)",
            response={
                "identity": [".ورودی نامعتبر است. لطفاً یک ایمیل یا شماره تلفن معتبر وارد کنید"],
                "cf_turnstile_response": [".اعتبارسنجی کپچا ناموفق بود"]
            },
            examples=[
                OpenApiExample(
                    name="عدم ارسال شناسه",
                    value={"identity": [".وارد کردن ایمیل یا شماره تلفن الزامی است"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="شناسه کاربری خالی",
                    value={"identity": [".لطفاً ایمیل یا شماره تلفن را وارد کنید"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="ایمیل نامعتبر",
                    value={"identity": [".وارد کنید example@example.com ایمیل نامعتبر است. لطفاً یک ایمیل معتبر مانند"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="شماره موبایل نامعتبر",
                    value={"identity": [".ورودی نامعتبر است. لطفاً یک ایمیل یا شماره تلفن معتبر وارد کنید"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="کپچای نامعتبر",
                    value={"cf_turnstile_response": [".اعتبارسنجی کپچا ناموفق بود"]},
                    response_only=True,
                ),
            ]
        ),
        403: STANDARD_ERROR_RESPONSES[403],
        429: STANDARD_ERROR_RESPONSES[429],
        500: STANDARD_ERROR_RESPONSES[500],
    },
    "summary": "درخواست بازیابی رمز عبور",
    "description": (
        "This API receives a user identifier (email or phone number) and sends a password reset verification code or link.\n\n" 
        "- CAPTCHA is required ✅ (`cf_turnstile_response` field)\n"
        "- The identifier can be either an email or a phone number 📧📱\n"
        "- Logged-in users are not allowed to use this service 🚫\n"
        "- Request rate limiting (Throttle) is enabled 2 min ⏱️\n"
        "- Sends OTP for phone numbers and email links for email addresses 📨\n"
        "- Only existing users can request password reset 👤"
    ),
    "tags": ["password"],
    "auth": [],  # No authentication required for this endpoint
}