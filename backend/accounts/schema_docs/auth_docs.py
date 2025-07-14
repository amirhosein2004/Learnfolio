from drf_spectacular.utils import OpenApiResponse
from accounts.serializers import IdentitySerializer

identity_submit_schema = {
    "request": IdentitySerializer,
    "responses": {
        200: OpenApiResponse(
            description="کد تایید یا لینک تایید با موفقیت ارسال شد.",
            examples=[{"detail": "کد تایید ارسال شد."}]
        ),
        400: OpenApiResponse(
            description="ورودی نامعتبر.",
            examples=[{"identity": ["ورودی نامعتبر است."]}]
        ),
        429: OpenApiResponse(
            description="تعداد درخواست‌ها بیش از حد مجاز است.",
            examples=[{"detail": "محدودیت نرخ درخواست فعال شده است."}]
        ),
        500: OpenApiResponse(
            description="خطای داخلی سرور.",
            examples=[{"detail": "خطای ناشناخته‌ای رخ داده است."}]
        ),
    },
    "summary": "ارسال شناسه کاربر و دریافت کد تایید",
    "description": "شماره موبایل یا ایمیل را دریافت می‌کند و کد تایید یا لینک تایید ارسال می‌کند.",
    "tags": ["Authentication"]
}