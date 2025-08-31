from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from accounts.api.v1.serializers.profile_serializers import AdminProfileSerializer
from ..common_schemas import STANDARD_ERROR_RESPONSES

admin_profile_get_schema = {
    "responses": {
        200: OpenApiResponse(
            description=".اطلاعات پروفایل ادمین با موفقیت دریافت شد",
            response=AdminProfileSerializer,
            examples=[
                OpenApiExample(
                    name="پروفایل ادمین کامل",
                    value={
                        "social_networks": {
                            "instagram": "https://instagram.com/admin",
                            "telegram": "https://t.me/admin",
                            "linkedin": "https://linkedin.com/in/admin",
                            "github": "https://github.com/admin"
                        },
                        "description": "مدیر سیستم آموزشی لرن‌فولیو"
                    },
                    response_only=True,
                ),
                OpenApiExample(
                    name="پروفایل ادمین خالی",
                    value={
                        "social_networks": "",
                        "description": ""
                    },
                    response_only=True,
                ),
            ]
        ),
        401: STANDARD_ERROR_RESPONSES[401],
        403: OpenApiResponse(
            description=".کاربر دسترسی ادمین ندارد",
            response={"detail": ".شما به این بخش دسترسی ندارید"},
            examples=[
                OpenApiExample(
                    name="عدم دسترسی ادمین",
                    value={"detail": ".شما به این بخش دسترسی ندارید"},
                    response_only=True,
                )
            ]
        ),
        500: STANDARD_ERROR_RESPONSES[500],
    },
    "summary": "دریافت اطلاعات پروفایل ادمین",
    "description": (
        "This API returns the admin user's profile information.\n\n"
        "- Admin authentication is required ✅\n"
        "- Returns admin's social networks and description\n"
        "- Only staff users can access this endpoint\n"
        "- Request rate limiting (Throttle) is enabled ⏱️"
    ),
    "tags": ["profile"],
}

admin_profile_patch_schema = {
    "request": AdminProfileSerializer,
    "responses": {
        200: OpenApiResponse(
            description=".پروفایل ادمین با موفقیت به‌روزرسانی شد",
            response={"detail": ".پروفایل ادمین با موفقیت به‌روزرسانی شد"},
            examples=[
                OpenApiExample(
                    name="به‌روزرسانی موفق",
                    value={"detail": ".پروفایل ادمین با موفقیت به‌روزرسانی شد"},
                    response_only=True,
                ),
            ]
        ),
        400: OpenApiResponse(
            description=".خطاهای اعتبارسنجی شبکه‌های اجتماعی یا توضیحات",
            response={
                "social_networks": [".فرمت شبکه‌های اجتماعی معتبر نیست"],
                "description": [".توضیحات باید حداکثر 1000 حرف باشد"]
            },
            examples=[
                OpenApiExample(
                    name="شبکه‌های اجتماعی نامعتبر",
                    value={"social_networks": [".شبکه‌های اجتماعی باید به صورت دیکشنری باشد"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="پلتفرم غیرمجاز",
                    value={"social_networks": [".مجاز نیست tiktok پلتفرم"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="لینک نامعتبر",
                    value={"social_networks": [".مجاز نیست instagram لینک"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="توضیحات طولانی",
                    value={"description": [".توضیحات باید حداکثر 1000 حرف باشد"]},
                    response_only=True,
                ),
            ]
        ),
        401: STANDARD_ERROR_RESPONSES[401],
        403: OpenApiResponse(
            description=".کاربر دسترسی ادمین ندارد",
            response={"detail": ".شما به این بخش دسترسی ندارید"},
            examples=[
                OpenApiExample(
                    name="عدم دسترسی ادمین",
                    value={"detail": ".شما به این بخش دسترسی ندارید"},
                    response_only=True,
                )
            ]
        ),
        429: STANDARD_ERROR_RESPONSES[429],
        500: STANDARD_ERROR_RESPONSES[500],
    },
    "summary": "به‌روزرسانی پروفایل ادمین",
    "description": (
        "This API allows admin users to update their profile information.\n\n"
        "- Admin authentication is required ✅\n"
        "- Can update social networks and description\n"
        "- Social networks must be valid URLs from allowed platforms\n"
        "- Description has a maximum length of 1000 characters\n"
        "- Request rate limiting (Throttle) is enabled ⏱️"
    ),
    "tags": ["profile"],
}
