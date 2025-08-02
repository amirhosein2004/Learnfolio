from accounts.services.cache_services import OTPCacheService
from core.tasks import send_email_task, send_sms_task
from accounts.utils.token_utils import generate_email_token

# TODO: بعدا بیا سیستم پیامکی رو برای اون شرکتی که قرار داد بستی پیاده سازی اش کن
def send_otp_for_phone(phone_number: str, purpose: str) -> str:
    """
    Generates and sends an OTP code via SMS for the given phone number.

    Args:
        phone_number (str): Recipient's phone number.
        purpose (str): Purpose of the OTP (e.g., 'login', 'register', 'reset password').

    Returns:
        str: The generated OTP code.

    """
    otp = OTPCacheService.generate_otp(phone_number=phone_number, purpose=purpose)
    message = f"{otp}:کد تایید شما"

    # Send SMS asynchronously via Celery
    send_sms_task.delay(phone_number, message)

    return otp

def send_auth_email(email: str, purpose: str) -> str:
    """
    Sends either an OTP code or a confirmation link to the user's email.

    Args:
        email (str): Recipient's email address.
        purpose (str): Purpose of the verification (e.g., 'login', 'register', 'reset password').

    Returns:
        str: The OTP code or confirmation link.
    """
    if purpose == "register":
        token = generate_email_token(email, purpose)
        link = f"http://localhost:8000/api/auth/verify-otp-or-link/?email={email}&token={token}&purpose={purpose}"
        subject = "لینک تایید ایمیل"
        message = f"برای ادامه عملیات ، روی لینک زیر کلیک کنید:\n\n{link}\n\nاین لینک تا ۱۵ دقیقه معتبر است"

        # Send verification link via Celery task
        send_email_task.delay(email, subject, message)
        return link

    else:
        otp = OTPCacheService.generate_otp(email=email, purpose=purpose)
        subject = "کد تایید"
        message = f"{otp}:کد تایید شما"

        # Generate and send OTP via email
        send_email_task.delay(email, subject, message)
        return otp

