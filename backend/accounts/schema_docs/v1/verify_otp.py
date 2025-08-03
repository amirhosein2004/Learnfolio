from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from accounts.api.v1.serializers.auth_serializers import OTPVerificationSerializer
from .common_schemas import STANDARD_ERROR_RESPONSES

otp_verification_schema = {
    "request": OTPVerificationSerializer,
    "responses": {
        200: OpenApiResponse(
            description=".احراز هویت موفقیت‌آمیز انجام شد",
            response={
                "detail": "پیام موفقیت‌آمیز",
                "action": "login | register",
                "access": "توکن دسترسی JWT",
                "refresh": "توکن رفرش JWT"
            },
            examples=[
                OpenApiExample(
                    name="ورود موفق",
                    value={
                        "detail": ".ورود با موفقیت انجام شد",
                        "action": "login",
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                    },
                    response_only=True,
                ),
                OpenApiExample(
                    name="ثبت‌نام موفق",
                    value={
                        "detail": ".ثبت نام با موفقیت انجام شد",
                        "action": "register",
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                    },
                    response_only=True,
                ),
            ]
        ),
        400: OpenApiResponse(
            description=".خطاهای اعتبارسنجی ورودی‌ها",
            response={
                "identity": [".خطای مربوط به شناسه"],
                "otp": [".خطای مربوط به کد تایید"],
                "cf_turnstile_response": [".خطای مربوط به کپچا"]
            },
            examples=[
                OpenApiExample(
                    name="عدم ارسال شناسه",
                    value={"identity": [".وارد کردن ایمیل یا شماره تلفن الزامی است"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="ایمیل نامعتبر",
                    value={"identity": [".وارد کنید example@example.com ایمیل نامعتبر است. لطفاً یک ایمیل معتبر مانند"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="کد تایید نامعتبر",
                    value={"otp": [".کد تایید باید 6 رقم باشد"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="کد تأیید غیر عددی",
                    value={"otp": [".کد تأیید باید فقط شامل ارقام باشد"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="کد تایید منقضی شده",
                    value={"otp": [".کد وارد شده اشتباه یا منقضی شده است. لطفاً دوباره تلاش کنید"]},
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
    "summary": "تایید کد OTP و احراز هویت کاربر",
        "description": (
        "This API is used to verify the OTP code sent to the user's email or mobile number.\n\n"
        "- Requires CAPTCHA token (Cloudflare Turnstile) ✅\n"
        "- The user identifier can be either email or mobile number (supports Persian/Arabic digits) 🔄\n"
        "- Authenticated users are not allowed to use this API 🚫\n"
        "- Request rate limiting (Throttle) is enabled: 2 minutes⏱️\n\n"
        "On success, JWT tokens for authentication are returned."
    ),
    "tags": ["auth"],
    "auth": [],  # No authentication required for this endpoint
}