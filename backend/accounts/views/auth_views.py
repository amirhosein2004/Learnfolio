import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import IdentitySerializer
from accounts.services.auth_services import handle_identity_submission
from drf_spectacular.utils import extend_schema
from accounts.schema_docs.auth_docs import identity_submit_schema
from core.throttles.throttles import CustomAnonThrottle
from core.utils.captcha import verify_turnstile_token
from core.utils.network import get_client_ip

logger = logging.getLogger(__name__)

@extend_schema(**identity_submit_schema)
class IdentitySubmissionAPIView(APIView):
    """
    Handles identity submission (email or phone) and sends an OTP or confirmation link.

    For authenticated users: sends OTP to email or phone.
    For anonymous users: sends OTP to phone or a confirmation link to email.
    Includes CAPTCHA validation (Turnstile) to prevent malicious requests.

    Rate-limited via CustomAnonThrottle(return 429 Too Many Requests).
    """
    throttle_classes = [CustomAnonThrottle] # Prevent abuse by limiting request rate

    def post(self, request):
        """
        POST method to validate submitted identity (email or phone)
        and trigger OTP or confirmation link sending.

        The captcha token must be sent from the client side in the `cf-turnstile-response` field.
        """
        captcha_token = request.data.get("cf-turnstile-response")
        remote_ip = get_client_ip(request)

        if not verify_turnstile_token(captcha_token, remoteip=remote_ip):
            logger.warning(f"Captcha validation failed for IP {remote_ip}")
            return Response(
                {"detail": ".اعتبارسنجی کپچا ناموفق بود"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
        serializer = IdentitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        identity = serializer.validated_data['identity']

        logger.info(f"Identity submission attempt by {identity} from IP {remote_ip}")

        try:
            message = handle_identity_submission(identity)
            logger.info(f"OTP/link sent successfully for {identity} from IP {remote_ip}")
            return Response({'detail': message}, status=200)
        except Exception as e:
            logger.error(f"Error processing identity submission for {identity} from IP {remote_ip}", exc_info=True)
            return Response({'detail': ".خطای ناشناخته‌ای رخ داده است لطفا دوباره تلاش کنید"}, status=500)       