from drf_spectacular.utils import OpenApiResponse, OpenApiParameter
from accounts.serializers import IdentitySerializer

identity_submit_schema = {
    "request": IdentitySerializer,
    "responses": {
        200: OpenApiResponse(
            description="کد تایید یا لینک تایید با موفقیت ارسال شد.",
            examples=[{"detail": "کد تایید ارسال شد."}]
        ),
        400: OpenApiResponse(
            description="ورودی نامعتبر یا اعتبارسنجی کپچا ناموفق بود.",
            examples=[
                {"identity": ["ورودی نامعتبر است."]},
                {"detail": "اعتبارسنجی کپچا ناموفق بود."}
            ]
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
    "description": (
        "این API شماره موبایل یا ایمیل کاربر را دریافت می‌کند و در صورت اعتبارسنجی موفق، "
        "کد تایید (OTP) یا لینک تایید را ارسال می‌کند.\n\n"
        "📌 **اعتبارسنجی کپچا (Turnstile)** الزامی است. "
        "`cf-turnstile-response` باید در `request.data` ارسال شود.\n\n"
        "🧠 برای کاربران ناشناس، محدودیت نرخ درخواست (Rate limit) فعال است.\n"
        "🔐 این عملیات نیاز به احراز هویت ندارد اما محافظت شده با کپچا و throttle است."
    ),
    "tags": ["Authentication"],
    "parameters": [
        OpenApiParameter(
            name="cf-turnstile-response",
            type=str,
            location=OpenApiParameter.QUERY,
            required=True,
            description="توکن کپچا Turnstile که از سمت کلاینت (فرانت‌اند) ارسال می‌شود."
        )
    ]
}
