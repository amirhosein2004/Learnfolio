from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from accounts.api.v1.serializers.password_serializers import SetResetPasswordSerializer
from accounts.schema_docs.v1.common_schemas import STANDARD_ERROR_RESPONSES

reset_password_schema = {
    "request": SetResetPasswordSerializer,
    "responses": {
        200: OpenApiResponse(
            description=".رمز عبور با موفقیت تغییر یافت",
            response={
                "detail": ".رمز عبور تغییر یافت"
            },
            examples=[
                OpenApiExample(
                    name="تغییر موفق رمز عبور",
                    value={
                        "detail": ".رمز عبور تغییر یافت"
                    },
                    response_only=True,
                ),
            ]
        ),
        400: OpenApiResponse(
            description=".خطاهای اعتبارسنجی توکن بازیابی، رمز عبور یا کپچا",
            response={
                "reset_token": [".شما نمی‌توانید این کار را انجام دهید، لطفا دوباره امتحان کنید"],
                "new_password": [".رمز عبور جدید الزامی است"],
                "confirm_password": [".تایید رمز عبور الزامی است"],
                "detail": [".رمزهای عبور مطابقت ندارند"],
                "cf_turnstile_response": [".اعتبارسنجی کپچا ناموفق بود"]
            },
            examples=[
                OpenApiExample(
                    name="عدم ارسال توکن بازیابی",
                    value={"reset_token": [".توکن ریست پسورد الزامی است"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="توکن بازیابی خالی",
                    value={"reset_token": [".توکن ریست پسورد خالی است"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="توکن بازیابی نامعتبر",
                    value={"reset_token": [".شما نمی‌توانید این کار را انجام دهید، لطفا دوباره امتحان کنید"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="عدم ارسال رمز عبور جدید",
                    value={"new_password": [".رمز عبور جدید الزامی است"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="رمز عبور جدید خالی",
                    value={"new_password": [".رمز عبور جدید خالی است"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="رمز عبور ضعیف",
                    value={"new_password": [".رمز عبور باید حداقل ۸ کاراکتر باشد"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="عدم ارسال تایید رمز عبور",
                    value={"confirm_password": [".تایید رمز عبور الزامی است"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="تایید رمز عبور خالی",
                    value={"confirm_password": [".تایید رمز عبور خالی است"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="عدم تطابق رمزهای عبور",
                    value={"detail": [".رمزهای عبور مطابقت ندارند"]},
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
    "summary": "تنظیم رمز عبور جدید پس از بازیابی",
    "description": (
        "This API allows users to set a new password after successful verification using reset token.\n\n" 
        "- CAPTCHA is required ✅ (`cf_turnstile_response` field)\n"
        "- Requires valid reset token from previous verification step 🔑\n"
        "- Logged-in users are not allowed to use this service 🚫\n"
        "- Request rate limiting (Throttle) is enabled ⏱️\n"
        "- Password must meet security requirements 🔐\n"
        "- New password and confirmation must match ✅\n"
        "- Reset token has expiry time limit (10 minutes) ⏰"
    ),
    "tags": ["password"],
    "auth": [],  # No authentication required for this endpoint
}