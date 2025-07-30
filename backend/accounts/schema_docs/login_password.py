from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from accounts.serializers.auth_serializers import PasswordLoginSerializer
from accounts.schema_docs.common_schemas import STANDARD_ERROR_RESPONSES

password_login_schema = {
    "request": PasswordLoginSerializer,
    "responses": {
        200: OpenApiResponse(
            description=".ورود با رمز عبور با موفقیت انجام شد",
            response={
                "detail": "پیام موفقیت‌آمیز به فارسی",
                "access": "توکن دسترسی JWT",
                "refresh": "توکن تازه‌سازی JWT"
            },
            examples=[
                OpenApiExample(
                    name="ورود موفق با ایمیل",
                    value={
                        "detail": "کاربر با موفقیت وارد شد",
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                    },
                    response_only=True,
                ),
                OpenApiExample(
                    name="ورود موفق با شماره موبایل",
                    value={
                        "detail": "کاربر با موفقیت وارد شد",
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                    },
                    response_only=True,
                ),
            ]
        ),
        400: OpenApiResponse(
            description=".خطاهای اعتبارسنجی شناسه، رمز عبور یا کپچا",
            response={
                "identity": [".ورودی نامعتبر است. لطفاً یک ایمیل یا شماره تلفن معتبر وارد کنید"],
                "password": [".رمز عبور باید حداقل ۸ کاراکتر باشد"],
                "cf_turnstile_response": [".اعتبارسنجی کپچا ناموفق بود"],
                "detail": [".کاربر وجود ندارد یا رمز اشتباه است"]
            },
            examples=[
                OpenApiExample(
                    name="عدم ارسال شناسه",
                    value={"identity": [".وارد کردن ایمیل یا شماره تلفن الزامی است"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="شناسه کاربری خالی",
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
                    name="رمز عبور خالی",
                    value={"password": [".رمز عبور نمی‌تواند خالی باشد"]},
                    response_only=True
                ),
                OpenApiExample(
                    name="رمز عبور کوتاه",
                    value={"password": [".رمز عبور باید حداقل ۸ کاراکتر باشد"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="عدم ارسال رمز عبور",
                    value={"password": [".وارد کردن رمز عبور الزامی است"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="کاربر وجود ندارد",
                    value={"detail": [".کاربر وجود ندارد یا رمز اشتباه است"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name=" رمز عبور اشتباه یا هنوز ندارد",
                    value={"detail": [".رمز عبور اشتباه است یا هنوز تنظیم نشده است"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="کپچای نامعتبر",
                    value={"cf_turnstile_response": [".اعتبارسنجی کپچا ناموفق بود"]},
                    response_only=True,
                ),
            ]
        ),
        **STANDARD_ERROR_RESPONSES # Include standard error responses
    },
    "summary": "ورود با رمز عبور",
    "description": (
        "This API authenticates users using their identity (email or phone) and password.\n\n" 
        "- CAPTCHA is required ✅ (`cf_turnstile_response` field)\n"
        "- The identifier can be either an email or a phone number 📧📱\n"
        "- Password must be at least 8 characters long 🔐\n"
        "- Logged-in users are not allowed to use this service 🚫\n"
        "- Request rate limiting (Throttle) is enabled 🛡️\n"
        "- Returns JWT tokens upon successful authentication 🔑\n"
        "- Supports both existing users with passwords and new users who set passwords\n"
        "- Validates user existence and password correctness before authentication"
    ),
    "tags": ["auth"],
    "auth": [],  # No authentication required for this endpoint
}