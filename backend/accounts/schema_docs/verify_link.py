from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from accounts.serializers.auth_serializers import EmailConfirmationLinkSerializer
from accounts.schema_docs.common_schemas import STANDARD_ERROR_RESPONSES

link_verification_schema = {
    "request": EmailConfirmationLinkSerializer,
    "responses": {
        200: OpenApiResponse(
            description=".لینک تأیید با موفقیت احراز هویت شد",
            response={
                "detail": "پیام موفقیت‌آمیز به فارسی",
                "action": "register",
                "access": "توکن دسترسی JWT",
                "refresh": "توکن تازه‌سازی JWT"
            },
            examples=[
                OpenApiExample(
                    name="ثبت‌نام موفق با ایمیل",
                    value={
                        "detail": ".لینک با موفقیت تایید شد",
                        "action": "register",
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                    },
                    response_only=True,
                ),
            ]
        ),
        400: OpenApiResponse(
            description=".خطاهای اعتبارسنجی کپچا، توکن یا شناسه",
            response={
                "identity": [".برای تایید لینک ایمیل، لطفاً یک آدرس ایمیل معتبر وارد کنید"],
                "token": [".توکن منقضی شده است. لطفاً مجدداً درخواست دهید"],
                "cf_turnstile_response": [".اعتبارسنجی کپچا ناموفق بود"]
            },
            examples=[
                OpenApiExample(
                    name="ایمیل نامعتبر",
                    value={"identity": [".برای تایید لینک ایمیل، لطفاً یک آدرس ایمیل معتبر وارد کنید"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="ایمیل تکراری",
                    value={"identity": [".این ایمیل قبلاً ثبت شده است"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="توکن نامعتبر",
                    value={"token": [".توکن نامعتبر است"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="توکن منقضی شده",
                    value={"token": [".توکن منقضی شده است. لطفاً مجدداً درخواست دهید"]},
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
    "summary": "تأیید لینک ثبت‌نام از طریق ایمیل",
    "description": (
        "This API verifies email confirmation links for user registration.\n\n" 
        "- CAPTCHA is required ✅ (`cf_turnstile_response` field)\n"
        "- Only email addresses are accepted (not phone numbers) 📧\n"
        "- Token must be valid and not expired (15 minutes max) ⏱️\n"
        "- Logged-in users are not allowed to use this service 🚫\n"
        "- Request rate limiting (Throttle) is enabled 2 min⏱️\n"
        "- Returns JWT tokens upon successful verification 🔑"
    ),
    "tags": ["auth"],
    "auth": [],  # No authentication required for this endpoint
}