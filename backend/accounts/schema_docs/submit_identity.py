from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from accounts.serializers.auth_serializers import IdentitySerializer
from accounts.schema_docs.common_schemas import STANDARD_ERROR_RESPONSES

identity_submit_schema = {
    "request": IdentitySerializer,
    "responses": {
        200: OpenApiResponse(
            description=".کد یا لینک تأیید با موفقیت ارسال شد",
            response={
                "message": "پیام موفقیت‌آمیز به فارسی",
                "purpose": "login | register",
                "next_step": "آدرس مرحله بعد"
            },
            examples=[
                OpenApiExample(
                    name="ورود با ایمیل",
                    value={
                        "message": ".کد ورود به ایمیل شما ارسال شد",
                        "purpose": "login",
                        "next_step": "/api/accounts/verify-otp/"
                    },
                    response_only=True,
                ),
                OpenApiExample(
                    name="ورود با شماره موبایل",
                    value={
                        "message": ".کد ورود برای شماره شما ارسال شد",
                        "purpose": "login",
                        "next_step": "/api/accounts/verify-otp/"
                    },
                    response_only=True,
                ),
                OpenApiExample(
                    name="ثبت‌نام با ایمیل",
                    value={
                        "message": ".لینک ثبت‌نام به ایمیل شما ارسال شد",
                        "purpose": "register",
                        "next_step": "/api/accounts/verify-link/"
                    },
                    response_only=True,
                ),
                OpenApiExample(
                    name="ثبت‌نام با شماره موبایل",
                    value={
                        "message": ".کد ثبت‌نام برای شماره شما ارسال شد",
                        "purpose": "register",
                        "next_step": "/api/accounts/verify-otp/"
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
        **STANDARD_ERROR_RESPONSES # Include standard error responses
    },
    "summary": "ارسال شناسه (ایمیل یا موبایل) و دریافت کد تأیید",
    "description": (
        "This API receives a user identifier (email or phone number) and, if valid, sends a verification code.\n\n" 
        "- CAPTCHA is required ✅ (`cf_turnstile_response` field)\n"
        "- The identifier can be either an email or a phone number. Persian/Arabic digits are also supported 🔄\n"
        "- Logged-in users are not allowed to use this service 🚫\n"
        "- Request rate limiting (Throttle) is enabled 2 min⏱️"
    ),
    "tags": ["auth"],
    "auth": [],  # No authentication required for this endpoint
}