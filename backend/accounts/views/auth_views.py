from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import IdentitySerializer
from accounts.services.auth_services import handle_identity_submission
from drf_spectacular.utils import extend_schema, OpenApiResponse
from core.throttles.throttles import CustomAnonThrottle

class IdentitySubmissionAPIView(APIView):
    """
    Handles identity submission (email or phone) and sends an OTP or confirmation link.

    For authenticated users: sends OTP to email or phone.
    For anonymous users: sends OTP to phone or a confirmation link to email.

    Rate-limited via CustomAnonThrottle(return 429 Too Many Requests).
    """
    throttle_classes = [CustomAnonThrottle] # Prevent abuse by limiting request rate

    @extend_schema(
    request=IdentitySerializer,
    responses={
        200: OpenApiResponse(
            description=(
                "کد تأیید (OTP) یا لینک تأیید با موفقیت ارسال شد.\n"
                "- اگر ورودی شماره موبایل ایرانی باشد، کد تأیید از طریق پیامک ارسال می‌شود.\n"
                "- اگر ورودی ایمیل باشد، لینک تأیید از طریق ایمیل ارسال می‌شود."
            ),
            examples=[
                {"detail": "کد تایید به شماره موبایل شما ارسال شد."},
                {"detail": "لینک تایید به ایمیل شما ارسال شد."},
            ],
        ),
        400: OpenApiResponse(
            description="ورودی نامعتبر: ایمیل یا شماره موبایل معتبر نیست.",
            examples=[
                {"identity": ["ورودی نامعتبر است. لطفاً یک ایمیل یا شماره تلفن معتبر وارد کنید"]}
            ],
        ),
        429: OpenApiResponse(
            description="تعداد درخواست‌ها بیش از حد مجاز است (Rate Limiting).",
            examples=[
                {"detail": "درخواست‌های شما بیش از حد مجاز است. لطفا کمی صبر کنید."}
            ],
        ),
        500: OpenApiResponse(
            description="خطای داخلی سرور (خطای ناشناخته).",
            examples=[
                {"detail": "خطای ناشناخته‌ای رخ داده است لطفا دوباره تلاش کنید"}
            ],
        ),
    },
    summary="ارسال شناسه کاربر (ایمیل یا شماره موبایل) و دریافت کد تایید یا لینک",
    description=(
        "این Endpoint برای دریافت شناسه‌ی کاربر (ایمیل یا شماره موبایل ایرانی) طراحی شده و پس از بررسی، یک کد تأیید (OTP) یا لینک تأیید برای کاربر ارسال می‌کند:\n"
        "- اگر ورودی ایمیل باشد، لینک یا کد از طریق ایمیل ارسال می‌شود.\n"
        "- اگر ورودی شماره موبایل باشد، کد از طریق پیامک ارسال می‌شود.\n"
        "- برای جلوگیری از سوءاستفاده، محدودیت نرخ (Rate Limiting) برای این درخواست فعال است.\n\n"
        "📌 مقدار `identity` می‌تواند یکی از موارد زیر باشد:\n"
        "- شماره موبایل ایرانی (فرمت: 09xxxxxxxxx)\n"
        "- یا ایمیل معتبر\n\n"
        "مثال درخواست:\n"
        "```json\n{ \"identity\": \"09380186731\" }\n```\n\n"
        "روش: POST\n"
        "آدرس: /api/auth/submit-identity/\n"
        "هدرها: Content-Type: application/json"
    ),
    tags=["Authentication"],
    )
    
    def post(self, request):
        """
        POST method to validate submitted identity (email or phone)
        and trigger OTP or confirmation link sending.

        Returns:
            200 OK: if identity is valid and message is sent.
            500 Internal Server Error: if any unhandled error occurs.
        """
        serializer = IdentitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        identity = serializer.validated_data['identity']

        try:
            message = handle_identity_submission(identity)
            return Response({'detail': message}, status=200)
        except Exception as e:
            # logger.exception("Unhandled error in IdentitySubmissionView")
            return Response({'detail': ".خطای ناشناخته‌ای رخ داده است لطفا دوباره تلاش کنید"}, status=500)
