from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from accounts.api.v1.serializers.auth_serializers import IdentitySerializer
from ..common_schemas import STANDARD_ERROR_RESPONSES

resend_otp_or_link_schema = {
    "request": IdentitySerializer,
    "responses": {
        200: OpenApiResponse(
            description=".کد یا لینک تأیید با موفقیت مجدداً ارسال شد",
            response={
                "detail": "پیام موفقیت‌آمیز به فارسی",
                "purpose": "login | register",
                "next_url": "آدرس مرحله بعد"
            },
            examples=[
                OpenApiExample(
                    name="ارسال مجدد کد ورود با ایمیل",
                    value={
                        "detail": ".کد ورود به ایمیل شما ارسال شد",
                        "purpose": "login",
                        "next_url": "/api/v1/accounts/auth/verify-otp/"
                    },
                    response_only=True,
                ),
                OpenApiExample(
                    name="ارسال مجدد کد ورود با موبایل",
                    value={
                        "detail": ".کد ورود برای شماره شما ارسال شد",
                        "purpose": "login",
                        "next_url": "/api/v1/accounts/auth/verify-otp/"
                    },
                    response_only=True,
                ),
                OpenApiExample(
                    name="ارسال مجدد لینک ثبت‌نام با ایمیل",
                    value={
                        "detail": ".لینک ثبت‌نام به ایمیل شما ارسال شد",
                        "purpose": "register",
                        "next_url": "/api/v1/accounts/auth/verify-link/"
                    },
                    response_only=True,
                ),
                OpenApiExample(
                    name="ارسال مجدد کد ثبت‌نام با موبایل",
                    value={
                        "detail": ".کد ثبت‌نام برای شماره شما ارسال شد",
                        "purpose": "register",
                        "next_url": "/api/v1/accounts/auth/verify-otp/"
                    },
                    response_only=True,
                ),
            ]
        ),
        400: OpenApiResponse(
            description=".خطاهای اعتبارسنجی کپچا یا شناسه",
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
    "summary": "ارسال مجدد کد یا لینک تأیید",
    "description": (
        "This API resends verification OTP or confirmation link to the given identity.\n\n" 
        "- CAPTCHA is required ✅ (`cf_turnstile_response` field)\n"
        "- The identifier can be either an email or a phone number 📧📱\n"
        "- Logged-in users are not allowed to use this service 🚫\n"
        "- Resend cooldown: 2 minutes ⏱️\n"
        "- Automatically detects user status (existing/new) and sends appropriate verification:\n"
        "  • Existing users: Login OTP (email or phone)\n"
        "  • New users: Registration link (email) or OTP (phone)\n"
        "- Request rate limiting (Throttle) is enabled 🛡️"
    ),
    "tags": ["auth"],
    "auth": [],  # No authentication required for this endpoint
}