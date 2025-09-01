from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from accounts.api.v1.serializers.password_serializers import SetFirstTimePasswordSerializer
from accounts.schema_docs.v1.common_schemas import STANDARD_ERROR_RESPONSES

first_time_password_schema = {
    "request": SetFirstTimePasswordSerializer,
    "responses": {
        200: OpenApiResponse(
            description=".رمز عبور برای اولین بار با موفقیت تنظیم شد",
            response={
                "detail": "رمز عبور تغییر یافت"
            },
            examples=[
                OpenApiExample(
                    name="تنظیم موفق رمز عبور اولین بار",
                    value={
                        "detail": "رمز عبور تغییر یافت"
                    },
                    response_only=True,
                ),
            ]
        ),
        400: OpenApiResponse(
            description=".خطاهای اعتبارسنجی رمز عبور",
            response={
                "new_password": [".رمز عبور جدید الزامی است"],
                "confirm_password": [".تایید رمز عبور الزامی است"],
                "detail": [".رمزهای عبور مطابقت ندارند"]
            },
            examples=[
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
            ]
        ),
        401: STANDARD_ERROR_RESPONSES[401],
        429: STANDARD_ERROR_RESPONSES[429],
        500: STANDARD_ERROR_RESPONSES[500],
    },
    "summary": "تنظیم رمز عبور برای اولین بار",
    "description": (
        "This API allows authenticated users to set their password for the first time.\n\n" 
        "- User must be authenticated (logged in) 🔐\n"
        "- User must not have a password already set 🚫\n"
        "- Request rate limiting (Throttle) is enabled ⏱️\n"
        "- Password must meet security requirements 🔐\n"
        "- New password and confirmation must match ✅\n"
        "- Only for users who don't have a password yet 👤"
    ),
    "tags": ["password"],
}