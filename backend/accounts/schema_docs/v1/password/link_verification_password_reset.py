from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from accounts.api.v1.serializers.password_serializers import ResetPasswordConfirmationLinkSerializer
from accounts.schema_docs.v1.common_schemas import STANDARD_ERROR_RESPONSES

link_verification_password_reset_schema = {
    "request": ResetPasswordConfirmationLinkSerializer,
    "responses": {
        200: OpenApiResponse(
            description=".لینک تایید با موفقیت بررسی شد و توکن بازیابی صادر شد",
            response={
                "detail": "لینک تایید شد",
                "reset_token": "JWT token for password reset"
            },
            examples=[
                OpenApiExample(
                    name="تایید موفق لینک ایمیل",
                    value={
                        "detail": "لینک تایید شد",
                        "reset_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                    },
                    response_only=True,
                ),
            ]
        ),
        400: OpenApiResponse(
            description=".خطاهای اعتبارسنجی لینک تایید، شناسه یا کپچا",
            response={
                "identity": [".برای تایید لینک ایمیل، لطفاً یک آدرس ایمیل معتبر وارد کنید"],
                "token": [".توکن تایید لینک الزامی است"],
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
                    value={"identity": [".برای تایید لینک ایمیل، لطفاً یک آدرس ایمیل معتبر وارد کنید"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="عدم ارسال توکن لینک",
                    value={"token": [".توکن تایید لینک الزامی است"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="توکن تایید لینک خالی",
                    value={"token": [".توکن تایید لینک نمی‌تواند خالی باشد"]},
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
        403: STANDARD_ERROR_RESPONSES[403],
        429: STANDARD_ERROR_RESPONSES[429],
        500: STANDARD_ERROR_RESPONSES[500],
    },
    "summary": "تایید لینک ایمیل برای بازیابی رمز عبور",
    "description": (
        "This API verifies the email confirmation link for password reset and returns a reset token.\n\n" 
        "- CAPTCHA is required ✅ (`cf_turnstile_response` field)\n"
        "- Requires valid email address and confirmation token 📧\n"
        "- Logged-in users are not allowed to use this service 🚫\n"
        "- Request rate limiting (Throttle) is enabled ⏱️\n"
        "- Returns JWT reset token upon successful verification 🔑\n"
        "- Only works with email addresses, not phone numbers 📧\n"
        "- Link verification has expiry time limit ⏰"
    ),
    "tags": ["password"],
    "auth": [],  # No authentication required for this endpoint
}