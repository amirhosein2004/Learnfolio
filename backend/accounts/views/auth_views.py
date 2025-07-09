from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import IdentitySerializer
from accounts.services.auth_services import handle_identity_submission
from accounts.exceptions import EmailSendError, SmsSendError

class IdentitySubmissionView(APIView):
    """
    Receives email or phone and sends OTP or confirmation link.
    """

    def post(self, request):
        """
        Receive email or phone number and validate it.

        For logged-in users: send OTP to email or phone.
        For new users: send OTP to phone, send confirmation link to email.

        Returns a JSON response with the result message.
        """
        serializer = IdentitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        identity = serializer.validated_data['identity']

        try:
            message = handle_identity_submission(identity)
            return Response({'detail': message}, status=200)
        except (EmailSendError, SmsSendError) as e:
            # لاگ اختیاری: logger.warning(str(e))
            return Response({'detail': str(e)}, status=502)
        except Exception as e:
            # logger.exception("Unhandled error in IdentitySubmissionView")
            return Response({'detail': ".خطای ناشناخته‌ای رخ داده است"}, status=500)
