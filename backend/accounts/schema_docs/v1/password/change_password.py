from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from accounts.api.v1.serializers.password_serializers import ChangePasswordSerializer
from accounts.schema_docs.v1.common_schemas import STANDARD_ERROR_RESPONSES

change_password_schema = {
    "request": ChangePasswordSerializer,
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
            description=".خطاهای اعتبارسنجی رمز عبور فعلی یا جدید",
            response={
                "old_password": [".رمز عبور فعلی اشتباه است"],
                "new_password": [".رمز عبور جدید الزامی است"],
                "confirm_password": [".تایید رمز عبور الزامی است"],
                "detail": [".رمز فعلی و جدید نمیتوانند یکسان باشند"]
            },
            examples=[
                OpenApiExample(
                    name="عدم ارسال رمز عبور فعلی",
                    value={"old_password": [".رمز عبور فعلی الزامی است"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="رمز عبور فعلی خالی",
                    value={"old_password": [".رمز عبور فعلی خالی است"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="رمز عبور فعلی اشتباه",
                    value={"old_password": [".رمز عبور فعلی اشتباه است"]},
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
                    name="رمز فعلی و جدید یکسان",
                    value={"detail": [".رمز فعلی و جدید نمیتوانند یکسان باشند"]},
                    response_only=True,
                ),
            ]
        ),
        401: STANDARD_ERROR_RESPONSES[401],
        429: STANDARD_ERROR_RESPONSES[429],
        500: STANDARD_ERROR_RESPONSES[500],
    },
    "summary": "تغییر رمز عبور کاربر",
    "description": (
        "This API allows authenticated users to change their existing password.\n\n" 
        "- User must be authenticated (logged in) 🔐\n"
        "- User must have a password already set 🔑\n"
        "- Requires current password for verification 🔒\n"
        "- Request rate limiting (Throttle) is enabled ⏱️\n"
        "- New password must meet security requirements 🔐\n"
        "- New password and confirmation must match ✅\n"
        "- New password must be different from current password 🔄"
    ),
    "tags": ["password"],
}