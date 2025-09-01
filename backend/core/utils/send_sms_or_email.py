from kavenegar import KavenegarAPI, APIException, HTTPException
from django.conf import settings
from django.core.mail import send_mail
from core.exceptions.exceptions import SmsSendError, EmailSendError


def send_sms(phone_number: str, message: str) -> bool:
    """
    Sends an SMS message to the given phone number using Kavenegar API.

    Args:
        phone_number (str): The recipient's phone number.
        message (str): The text message to send.

    Raises:
        SmsSendError: If sending the SMS fails.
    """
    try:
        api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
        params = {
            'sender': '2000660110',
            'receptor': phone_number,
            'message': message,
        }
        api.sms_send(params)
    except (APIException, HTTPException) as e:
        error_msg = e.args[0].decode('utf-8') if isinstance(e.args[0], bytes) else str(e) # Decode error message
        raise SmsSendError(error_msg)


def send_email(to_email: str, subject: str, message: str) -> bool:
    """
    Sends an email using Django's email backend.

    Args:
        to_email (str): Recipient's email address.
        subject (str): Email subject line.
        message (str): Email body text.

    Raises:
        EmailSendError: If sending the email fails.
    """
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [to_email],
            fail_silently=False
        )
    except Exception as e:
        raise EmailSendError(str(e))