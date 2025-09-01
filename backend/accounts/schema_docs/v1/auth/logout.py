from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from ..common_schemas import STANDARD_ERROR_RESPONSES

logout_schema = {
    "request": {
        "application/json": {
            "type": "object",
            "properties": {
                "refresh": {
                    "type": "string",
                    "description": "توکن رفرش برای خروج از سیستم"
                }
            },
            "required": ["refresh"]
        }
    },
    "responses": {
        205: OpenApiResponse(
            description="خروج موفقیت‌آمیز از سیستم",
            response={
                "detail": ".با موفقیت خارج شدید"
            },
            examples=[
                OpenApiExample(
                    name="خروج موفق",
                    value={"detail": ".با موفقیت خارج شدید"},
                    response_only=True,
                ),
            ]
        ),
        400: OpenApiResponse(
            description=".خطاهای مربوط به توکن رفرش",
            response={
                "detail": ".خطا های مربوط به توکن رفرش مانند عدم ارسال یا نامعتبر بودن"
            },
            examples=[
                OpenApiExample(
                    name="عدم ارسال توکن رفرش",
                    value={"detail": ".لطفا توکن رفرش را ارسال کنید"},
                    response_only=True,
                ),
                OpenApiExample(
                    name="توکن نامعتبر یا منقضی",
                    value={"detail": ".توکن نامعتبر یا منقضی است"},
                    response_only=True,
                ),
            ]
        ),
        401: OpenApiResponse(
            description=".کاربر احراز هویت نشده است",
            response={
                "detail": ".ابتدا وارد شوید"
            },
            examples=[
                OpenApiExample(
                    name="عدم احراز هویت",
                    value={"detail": ".ابتدا وارد شوید"},
                    response_only=True,
                ),
            ]
        ),
        401: STANDARD_ERROR_RESPONSES[401],
        429: STANDARD_ERROR_RESPONSES[429],
        500: STANDARD_ERROR_RESPONSES[500],
    },
    "summary": "خروج کاربر از سیستم",
    "description": (
        "This API handles user logout by invalidating the refresh token.\n\n"
        "- Only authenticated users can access this endpoint 🔒\n"
        "- Requires the refresh token to be sent in the request body 📝\n"
        "- The refresh token will be blacklisted and invalidated 🚫\n"
        "- After logout, the user will need to authenticate again to access protected resources 🔑"
    ),
    "tags": ["auth"],
}