from accounts.models import OTP
from utils.send_sms_or_email import send_email, send_sms
from accounts.models import OTP
from accounts.exceptions import SmsSendError, EmailSendError
import secrets

# TODO: بعدا بیا سیستم پیامکی رو برای اون شرکتی که قرار داد بستی پیاده سازی اش کن
def send_otp_for_phone(phone_number: str, purpose: str):
    """
    Generates and sends an OTP code via SMS for the given phone number.

    Args:
        phone_number (str): Recipient's phone number.
        purpose (str): Purpose of the OTP (e.g., 'login', 'register', 'reset password').

    Returns:
        str: The generated OTP code.

    Raises:
        SmsSendError: If SMS sending fails.
    """
    try:
        otp_instance, _ = OTP.objects.generate_otp(phone_number=phone_number, purpose=purpose)
        message = f"کد شما: {otp_instance.code}"
        success = send_sms(phone_number, message)
        if not success:
            raise SmsSendError(f".ارسال پیامک ناموفق بود")
        return otp_instance.code
    except Exception as e:
        raise SmsSendError(".خطا در ارسال پیامک") from e

def send_auth_email(email: str, purpose: str, send_link: bool = False):
    """
    Sends either an OTP code or a confirmation link to the user's email.

    Args:
        email (str): Recipient's email address.
        purpose (str): Purpose of the verification (e.g., 'login', 'register', 'reset password').
        send_link (bool): If True, sends a confirmation link instead of a code.

    Returns:
        str: The OTP code or confirmation link.

    Raises:
        EmailSendError: If Email sending fails.
    """
    try:
        if send_link:
            token = secrets.token_urlsafe(32)
            # TODO: بعدا این بخش را هم کامل کن برای تایید ایمیل
            link = f"https://your-domain.com/verify-email/?email={email}&token={token}&purpose={purpose}"
            subject = "لینک تایید ایمیل"
            message = f"برای ادامه عملیات {purpose}، روی لینک زیر کلیک کنید:\n\n{link}\n\nاین لینک تا ۱۵ دقیقه معتبر است"
            success = send_email(email, subject, message)
            if not success:
                raise EmailSendError(f".ارسال ایمیل ناموفق بود")
            return link
        else:
            otp_instance, _ = OTP.objects.generate_otp(email=email, purpose=purpose)
            subject = "کد تایید ورود"
            message = f"{otp_instance.code} :برابر است با {purpose} کد تایید شما برای"
            success = send_email(email, subject, message)
            if not success:
                raise EmailSendError(f".ارسال ایمیل به ناموفق بود")
            return otp_instance.code
    except Exception as e:
        raise EmailSendError(".خطا در ارسال ایمیل") from e