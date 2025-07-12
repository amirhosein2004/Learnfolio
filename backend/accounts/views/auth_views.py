from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import IdentitySerializer
from accounts.services.auth_services import handle_identity_submission
from core.throttles.throttles import CustomAnonThrottle

class IdentitySubmissionAPIView(APIView):
    """
    Handles identity submission (email or phone) and sends an OTP or confirmation link.

    For authenticated users: sends OTP to email or phone.
    For anonymous users: sends OTP to phone or a confirmation link to email.

    Rate-limited via CustomAnonThrottle(return 429 Too Many Requests).
    """
    throttle_classes = [CustomAnonThrottle] # Prevent abuse by limiting request rate

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
