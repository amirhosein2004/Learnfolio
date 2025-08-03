from drf_spectacular.utils import OpenApiResponse, OpenApiExample

# پاسخ‌های خطای استاندارد
STANDARD_ERROR_RESPONSES = {
    403: OpenApiResponse(
        description=".کاربر وارد شده است و نمی‌تواند از این سرویس استفاده کند",
        response={"detail": ".شما قبلاً وارد شده‌اید"},
        examples=[
            OpenApiExample(
                name="کاربر وارد شده",
                value={"detail": ".شما قبلاً وارد شده‌اید"},
                response_only=True,
            )
        ]
    ),
    429: OpenApiResponse(
        description=".تعداد درخواست‌ها بیش از حد مجاز است",
        response={
            "detail": ".شما بیش از حد مجاز درخواست ارسال کرده‌اید. لطفاً بعداً تلاش کنید",
            "available_in_seconds": 45
        },
        examples=[
            OpenApiExample(
                name="محدودیت نرخ",
                value={
                    "detail": ".شما بیش از حد مجاز درخواست ارسال کرده‌اید. لطفاً بعداً تلاش کنید",
                    "available_in_seconds": 120
                },
                response_only=True,
            )
        ]
    ),
    500: OpenApiResponse(
        description=".خطای داخلی سمت سرور",
        response={"detail": ".خطای ناشناخته‌ای رخ داده است لطفا دوباره تلاش کنید"},
        examples=[
            OpenApiExample(
                name="خطای سرور",
                value={"detail": ".خطای ناشناخته‌ای رخ داده است لطفا دوباره تلاش کنید"},
                response_only=True,
            )
        ]
    ),
}
