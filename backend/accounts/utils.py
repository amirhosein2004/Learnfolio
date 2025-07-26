from accounts.models import OTP
from core.tasks import send_email_task, send_sms_task
from accounts.models import OTP
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from django.conf import settings 

# TODO: بعدا بیا سیستم پیامکی رو برای اون شرکتی که قرار داد بستی پیاده سازی اش کن
def send_otp_for_phone(phone_number: str, purpose: str):
    """
    Generates and sends an OTP code via SMS for the given phone number.

    Args:
        phone_number (str): Recipient's phone number.
        purpose (str): Purpose of the OTP (e.g., 'login', 'register', 'reset password').

    Returns:
        str: The generated OTP code.

    """
    otp_instance, _ = OTP.objects.generate_otp(phone_number=phone_number, purpose=purpose)
    message = f"کد شما: {otp_instance.code}"

    # Send SMS asynchronously via Celery
    send_sms_task.delay(phone_number, message)

    return otp_instance.code

def send_auth_email(email: str, purpose: str, send_link: bool = False):
    """
    Sends either an OTP code or a confirmation link to the user's email.

    Args:
        email (str): Recipient's email address.
        purpose (str): Purpose of the verification (e.g., 'login', 'register', 'reset password').
        send_link (bool): If True, sends a confirmation link instead of a code.

    Returns:
        str: The OTP code or confirmation link.
    """
    if send_link:
        token = generate_email_token(email, purpose)
        link = f"http://localhost:8000/api/auth/verify-otp-or-link/?email={email}&token={token}&purpose={purpose}"
        subject = "لینک تایید ایمیل"
        message = f"برای ادامه عملیات ، روی لینک زیر کلیک کنید:\n\n{link}\n\nاین لینک تا ۱۵ دقیقه معتبر است"

        # Send verification link via Celery task
        send_email_task.delay(email, subject, message)
        return link

    else:
        otp_instance, _ = OTP.objects.generate_otp(email=email, purpose=purpose)
        subject = "کد تایید ورود"
        message = f"{otp_instance.code} :برابر است با {purpose} کد تایید شما برای"

        # Generate and send OTP via email
        send_email_task.delay(email, subject, message)
        return otp_instance.code

def generate_email_token(email, purpose):
    """
    Generate a secure token for email verification purposes.
    Args:
        email (str): The user's email address.
        purpose (str): The purpose of the token (e.g., 'register', 'reset').
    Returns:
        str: The generated token as a string.
    """
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    return serializer.dumps({'email': email, 'purpose': purpose})


def verify_email_token(token, max_age=900):
    """
    Verify the given token and return the stored data (email and purpose).
    Args:
        token (str): The token to verify.
        max_age (int): Maximum age of the token in seconds (default: 900, 15 minutes).
    Returns:
        - The stored data as a dictionary if the token is valid.
        - An error message if the token is invalid.
    """
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        data = serializer.loads(token, max_age=max_age)
        return data, None  # None means no error
    except SignatureExpired:
        return None, "توکن منقضی شده است. لطفاً مجدداً درخواست دهید."
    except BadSignature:
        return None, "توکن نامعتبر است." # None means no data
    except Exception as e:
        return None, f"خطای نامشخص در اعتبارسنجی توکن: {e}"