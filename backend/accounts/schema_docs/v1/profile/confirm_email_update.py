from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from accounts.api.v1.serializers.profile_serializers import ConfirmationLinkEmailUpdateSerializer
from ..common_schemas import STANDARD_ERROR_RESPONSES

confirm_email_update_schema = {
    "request": ConfirmationLinkEmailUpdateSerializer,
    "responses": {
        200: OpenApiResponse(
            description=".ایمیل با موفقیت تغییر کرد",
            response={"detail": ".ایمیل با موفقیت تغیر کرد"},
            examples=[
                OpenApiExample(
                    name="تایید موفق",
                    value={"detail": ".ایمیل با موفقیت تغیر کرد"},
                    response_only=True,
                ),
            ]
        ),
        400: OpenApiResponse(
            description=".خطاهای اعتبارسنجی توکن تایید یا ایمیل",
            response={
                "identity": [".برای تایید لینک ایمیل، لطفاً یک آدرس ایمیل معتبر وارد کنید"],
                "token": [".توکن تایید لینک الزامی است"]
            },
            examples=[
                OpenApiExample(
                    name="عدم ارسال ایمیل",
                    value={"identity": [".وارد کردن ایمیل یا شماره تلفن الزامی است"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="ایمیل خالی",
                    value={"identity": [".لطفاً ایمیل یا شماره تلفن را وارد کنید"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="ایمیل نامعتبر",
                    value={"identity": [".وارد کنید example@example.com ایمیل نامعتبر است. لطفاً یک ایمیل معتبر مانند"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="شماره تلفن به جای ایمیل",
                    value={"identity": [".برای تایید لینک ایمیل، لطفاً یک آدرس ایمیل معتبر وارد کنید"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="ایمیل تکراری",
                    value={"identity": [".این ایمیل قبلاً ثبت شده است"]},
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
            ]
        ),
        401: STANDARD_ERROR_RESPONSES[401],
        429: STANDARD_ERROR_RESPONSES[429],
        500: STANDARD_ERROR_RESPONSES[500],
    },
    "summary": "تایید لینک برای تغییر ایمیل",
    "description": (
        "This API verifies the confirmation link and updates the user's email address.\n\n"
        "- Authentication is required ✅\n"
        "- Requires valid email address and confirmation token\n"
        "- Identity must be an email address (not phone number)\n"
        "- Email must be unique (not already registered)\n"
        "- Validates token against the email confirmation system\n"
        "- Request rate limiting (Throttle) is enabled ⏱️"
    ),
    "tags": ["profile"],
}
