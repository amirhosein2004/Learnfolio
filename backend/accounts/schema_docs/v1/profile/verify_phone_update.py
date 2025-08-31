from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from accounts.api.v1.serializers.profile_serializers import VerifyOTPUserPhoneUpdateSerilizer
from ..common_schemas import STANDARD_ERROR_RESPONSES

verify_otp_phone_update_schema = {
    "request": VerifyOTPUserPhoneUpdateSerilizer,
    "responses": {
        200: OpenApiResponse(
            description=".شماره تلفن با موفقیت تغییر کرد",
            response={"detail": ".شماره تلفن با موفقیت تغیر کرد"},
            examples=[
                OpenApiExample(
                    name="تایید موفق",
                    value={"detail": ".شماره تلفن با موفقیت تغیر کرد"},
                    response_only=True,
                ),
            ]
        ),
        400: OpenApiResponse(
            description=".خطاهای اعتبارسنجی کد OTP یا شماره تلفن",
            response={
                "identity": [".ورودی نامعتبر است. لطفاً یک ایمیل یا شماره تلفن معتبر وارد کنید"],
                "otp": [".کد تایید الزامی است"]
            },
            examples=[
                OpenApiExample(
                    name="عدم ارسال شناسه",
                    value={"identity": [".وارد کردن ایمیل یا شماره تلفن الزامی است"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="شناسه خالی",
                    value={"identity": [".لطفاً ایمیل یا شماره تلفن را وارد کنید"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="شماره تلفن نامعتبر",
                    value={"identity": [".ورودی نامعتبر است. لطفاً یک ایمیل یا شماره تلفن معتبر وارد کنید"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="شماره تکراری",
                    value={"identity": [".این شماره قبلاً ثبت شده است"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="عدم ارسال کد OTP",
                    value={"otp": [".کد تایید الزامی است"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="کد OTP خالی",
                    value={"otp": [".کد تایید نمی‌تواند خالی باشد"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="کد OTP کوتاه یا بلند",
                    value={"otp": [".کد تایید باید 6 رقم باشد"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="کد OTP غیرعددی",
                    value={"otp": [".کد تأیید باید فقط شامل ارقام باشد"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="کد تایید منقضی شده",
                    value={"otp": [".کد منقضی شده است. لطفاً دوباره درخواست دهید"]},
                    response_only=True,
                ),
                OpenApiExample(
                    name="کد نادرست",
                    value={"otp": [".کد وارد شده نادرست است"]},
                    response_only=True,
                ),
            ]
        ),
        401: STANDARD_ERROR_RESPONSES[401],
        429: STANDARD_ERROR_RESPONSES[429],
        500: STANDARD_ERROR_RESPONSES[500],
    },
    "summary": "تایید کد OTP برای تغییر شماره تلفن",
    "description": (
        "This API verifies the OTP code and updates the user's phone number.\n\n"
        "- Authentication is required ✅\n"
        "- Requires valid phone number and 6-digit OTP code\n"
        "- OTP must be numeric only\n"
        "- Phone number must be unique (not already registered)\n"
        "- Validates OTP against the provided phone number\n"
        "- Request rate limiting (Throttle) is enabled ⏱️"
    ),
    "tags": ["profile"],
}
