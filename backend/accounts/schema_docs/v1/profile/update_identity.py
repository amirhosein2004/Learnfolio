from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from accounts.api.v1.serializers.profile_serializers import UserPhoneOrEmailUpdateSerilizer
from ..common_schemas import STANDARD_ERROR_RESPONSES

user_update_identity_schema = {
    "request": UserPhoneOrEmailUpdateSerilizer,
    "responses": {
        200: OpenApiResponse(
            description=".درخواست تغییر ایمیل یا شماره تلفن با موفقیت ارسال شد",
            response={
                "detail": "پیام موفقیت‌آمیز به فارسی",
                "next_url": "آدرس مرحله بعد",
                "purpose": "update_phone | update_email"
            },
            examples=[
                OpenApiExample(
                    name="درخواست تغییر ایمیل",
                    value={
                        "detail": "لینک تایید به ایمیل ارسال شد",
                        "next_url": "/api/v1/accounts/profile/update-email/confirm/",
                        "purpose": "update_email"
                    },
                    response_only=True,
                ),
                OpenApiExample(
                    name="درخواست تغییر شماره تلفن",
                    value={
                        "detail": "کد تایید به شماره تلفن ارسال شد",
                        "next_url": "/api/v1/accounts/profile/update-phone/verify/",
                        "purpose": "update_phone"
                    },
                    response_only=True,
                ),
            ]
        ),
        400: OpenApiResponse(
            description=".خطاهای اعتبارسنجی شناسه (ایمیل یا شماره موبایل)",
            response={
                "identity": [".ورودی نامعتبر است. لطفاً یک ایمیل یا شماره تلفن معتبر وارد کنید"]
            },
            examples=[
                OpenApiExample(
                    name="عدم ارسال شناسه",
                    value={"identity": [".وارد کردن ایمیل یا شماره تلفن الزامی است"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="شناسه خالی",
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
                    name="شناسه تکراری",
                    value={"identity": [".این ایمیل قبلاً ثبت شده است"]},
                    response_only=True,
                ),
            ]
        ),
        401: STANDARD_ERROR_RESPONSES[401],
        429: STANDARD_ERROR_RESPONSES[429],
        500: STANDARD_ERROR_RESPONSES[500],
    },
    "summary": "درخواست تغییر ایمیل یا شماره تلفن",
    "description": (
        "This API initiates the process of updating user's email or phone number.\n\n"
        "- Authentication is required ✅\n"
        "- Accepts either email or phone number as identity\n"
        "- For email: sends confirmation link\n"
        "- For phone: sends OTP code\n"
        "- Identity must be unique (not already registered)\n"
        "- Sets 2-minute cooldown for resending\n"
        "- Request rate limiting (Throttle) is enabled ⏱️"
    ),
    "tags": ["profile"],
}
