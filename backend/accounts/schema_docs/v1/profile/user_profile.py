from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from accounts.api.v1.serializers.profile_serializers import UserProfileSerializer, UserFullNameSerializer
from ..common_schemas import STANDARD_ERROR_RESPONSES

user_profile_get_schema = {
    "responses": {
        200: OpenApiResponse(
            description=".اطلاعات پروفایل کاربر با موفقیت دریافت شد",
            response=UserProfileSerializer,
            examples=[
                OpenApiExample(
                    name="پروفایل کاربر",
                    value={
                        "full_name": "احمد محمدی",
                        "email": "ahmad@example.com",
                        "phone_number": "09123456789"
                    },
                    response_only=True,
                ),
                OpenApiExample(
                    name="پروفایل کاربر با مقادیر خالی",
                    value={
                        "full_name": "",
                        "email": "user@example.com",
                        "phone_number": ""
                    },
                    response_only=True,
                ),
            ]
        ),
        401: STANDARD_ERROR_RESPONSES[401],
        500: STANDARD_ERROR_RESPONSES[500],
    },
    "summary": "دریافت اطلاعات پروفایل کاربر",
    "description": (
        "This API returns the authenticated user's profile information.\n\n"
        "- Authentication is required ✅\n"
        "- Returns user's full name, email, and phone number\n"
        "- Null values are converted to empty strings\n"
        "- Request rate limiting (Throttle) is enabled ⏱️"
    ),
    "tags": ["profile"],
}

user_profile_patch_schema = {
    "request": UserFullNameSerializer,
    "responses": {
        200: OpenApiResponse(
            description=".نام و نام خانوادگی با موفقیت تغییر یافت",
            response={"detail": ".نام و نام خانوادگی با موفقیت تغییر یافت"},
            examples=[
                OpenApiExample(
                    name="به‌روزرسانی موفق",
                    value={"detail": ".نام و نام خانوادگی با موفقیت تغییر یافت"},
                    response_only=True,
                ),
            ]
        ),
        400: OpenApiResponse(
            description=".خطاهای اعتبارسنجی نام و نام خانوادگی",
            response={
                "full_name": [".نام و نام خانوادگی الزامی است"]
            },
            examples=[
                OpenApiExample(
                    name="نام خالی",
                    value={"full_name": [".نام و نام خانوادگی نمی تواند خالی باشد"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="نام کوتاه",
                    value={"full_name": [".نام و نام خانوادگی باید حداقل 2 حرف باشد"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="نام طولانی",
                    value={"full_name": [".نام و نام خانوادگی باید حداکثر 100 حرف باشد"]},
                    response_only=True,
                ),
            ]
        ),
        401: STANDARD_ERROR_RESPONSES[401],
        429: STANDARD_ERROR_RESPONSES[429],
        500: STANDARD_ERROR_RESPONSES[500],
    },
    "summary": "به‌روزرسانی نام و نام خانوادگی کاربر",
    "description": (
        "This API allows authenticated users to update their full name.\n\n"
        "- Authentication is required ✅\n"
        "- Full name must be between 2-100 characters\n"
        "- Full name cannot be blank\n"
        "- Request rate limiting (Throttle) is enabled ⏱️"
    ),
    "tags": ["profile"],
}

user_profile_delete_schema = {
    "responses": {
        200: OpenApiResponse(
            description=".حساب کاربری با موفقیت حذف شد",
            response={"detail": ".حساب کاربری شما با موفقیت حذف شد"},
            examples=[
                OpenApiExample(
                    name="حذف موفق",
                    value={"detail": ".حساب کاربری شما با موفقیت حذف شد"},
                    response_only=True,
                ),
            ]
        ),
        401: STANDARD_ERROR_RESPONSES[401],
        429: STANDARD_ERROR_RESPONSES[429],
        500: STANDARD_ERROR_RESPONSES[500],
    },
    "summary": "حذف حساب کاربری",
    "description": (
        "This API allows authenticated users to permanently delete their account.\n\n"
        "- Authentication is required ✅\n"
        "- This action is irreversible ⚠️\n"
        "- All user data will be permanently deleted\n"
        "- Request rate limiting (Throttle) is enabled ⏱️"
    ),
    "tags": ["profile"],
}
