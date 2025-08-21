from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from accounts.api.v1.serializers.password_serializers import ResetOTPVerificationSerializer
from accounts.schema_docs.v1.common_schemas import STANDARD_ERROR_RESPONSES

otp_verification_password_reset_schema = {
    "request": ResetOTPVerificationSerializer,
    "responses": {
        200: OpenApiResponse(
            description=".کد تایید با موفقیت بررسی شد و توکن بازیابی صادر شد",
            response={
                "detail": "کد تایید شد",
                "reset_token": "JWT token for password reset"
            },
            examples=[
                OpenApiExample(
                    name="تایید موفق کد OTP",
                    value={
                        "detail": "کد تایید شد",
                        "reset_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                    },
                    response_only=True,
                ),
            ]
        ),
        400: OpenApiResponse(
            description=".خطاهای اعتبارسنجی کد OTP، شناسه یا کپچا",
            response={
                "identity": [".ورودی نامعتبر است. لطفاً یک ایمیل یا شماره تلفن معتبر وارد کنید"],
                "otp": [".کد تأیید باید فقط شامل ارقام باشد"],
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
                    name="عدم ارسال کد",
                    value={"otp": [".کد تایید الزامی است"]},
                    response_only=True,
                ), 
                OpenApiExample(
                    name="کد تایید خالی",
                    value={"otp": [".کد تایید نمی‌تواند خالی باشد"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="طول کد تایید",
                    value={"otp": [".کد تایید باید 6 رقم باشد"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="کد تایید غیر عددی",
                    value={"otp": [".کد تأیید باید فقط شامل ارقام باشد"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="کد تایید منقضی شده",
                    value={"otp": [".کد منقضی شده است. لطفاً دوباره درخواست دهید"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="کد نادرست",
                    value={"otp": [".کد وارد شده نادرست است"]},
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
    "summary": "تایید کد OTP برای بازیابی رمز عبور",
    "description": (
        "This API verifies the OTP code sent to user's phone number for password reset and returns a reset token.\n\n" 
        "- CAPTCHA is required ✅ (`cf_turnstile_response` field)\n"
        "- Requires valid identity (phone number) and 6-digit OTP code 📱\n"
        "- Logged-in users are not allowed to use this service 🚫\n"
        "- Request rate limiting (Throttle) is enabled ⏱️\n"
        "- Returns JWT reset token upon successful verification 🔑\n"
        "- OTP must be exactly 6 digits and numeric only 🔢\n"
        "- OTP verification has expiry time limit ⏰"
    ),
    "tags": ["password"],
    "auth": [],  # No authentication required for this endpoint
}