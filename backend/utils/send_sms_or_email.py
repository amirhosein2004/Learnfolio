from kavenegar import KavenegarAPI, APIException, HTTPException
from django.conf import settings
from django.core.mail import send_mail


def send_sms(phone_number: str, message: str) -> bool:
    """
    Sends an SMS message to the given phone number using Kavenegar API.

    Args:
        phone_number (str): The recipient's phone number.
        message (str): The text message to send.

    Returns:
        bool: True if SMS was sent successfully, False otherwise.
    """
    try:
        api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
        params = {
            'sender': '2000660110',  # Optional sender ID
            'receptor': phone_number,
            'message': message,
        }
        api.sms_send(params)
        return True
    except (APIException, HTTPException) as e:
        # Ideally log this instead of print in production
        print(f"❌ SMS sending failed: {e.args[0].decode('utf-8') if isinstance(e.args[0], bytes) else str(e)}")

        return False


def send_email(to_email: str, subject: str, message: str) -> bool:
    """
    Sends an email using Django's email backend.

    Args:
        to_email (str): Recipient's email address.
        subject (str): Email subject line.
        message (str): Email body text.

    Returns:
        bool: True if email was sent successfully, False otherwise.
    """
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [to_email],
            fail_silently=False
        )
        return True
    except Exception as e:
        # Ideally log this instead of print in production
        print(f"❌ Email sending failed: {e}")
        return False