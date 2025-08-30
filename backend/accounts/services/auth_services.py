import logging
from typing import Any

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework_simplejwt.tokens import RefreshToken

from accounts.services.cache_services import OTPCacheService
from accounts.services.validation_services import get_identity_purpose
from accounts.utils.token_utils import generate_email_token
from core.tasks import send_email_task, send_sms_task

logger = logging.getLogger(__name__)

User = get_user_model()


def handle_identity_submission(identity: str) -> tuple[str, str, str]:
    """
    Sends an OTP or a confirmation link based on the user's identity.

    - If the user exists: send login code (email or phone).
    - If not: send signup link (email) or code (phone).

    Returns:
        tuple: (Result message,purpose, Next step URL)
    """
    purpose = get_identity_purpose(identity)

    if '@' in identity:
        if purpose == "register":
            # For registration, send confirmation link
            send_auth_email(email=identity, purpose=purpose)
            logger.info(f"Registration link sent to {identity}")
            return ".لینک ثبت‌نام به ایمیل شما ارسال شد", purpose, reverse('accounts_v1:verify_link')

        else:
            otp_code = send_auth_email(email=identity, purpose=purpose)
            logger.info(f"Login OTP sent to {identity}")
            return ".کد تایید به ایمیل شما ارسال شد", purpose, reverse('accounts_v1:verify_otp')
            
    else:
        otp_code = send_otp_for_phone(phone_number=identity, purpose=purpose)
        logger.info(f"OTP sent to phone {identity}")
        return f".کد تایید به شماره تلفن شما ارسال شد: {otp_code}", purpose, reverse('accounts_v1:verify_otp')


def login_or_register_user(identity: str) -> tuple[User, str, str]:
    """
    Log in or register a user based on their identity (email or phone number).
    """
    purpose = get_identity_purpose(identity)
    is_email = '@' in identity
    
    if purpose == "register":
        # register new user
        create_kwargs = {'email': identity} if is_email else {'phone_number': identity}
        user = User.objects.create_user(**create_kwargs)
        message = ".ایمیل با موفقیت تأیید شد" if is_email else ".ثبت نام با موفقیت انجام شد"
        action = "register"
        logger.info(f"User registered: {user.id}")
    else:
        # login existing user
        filter_kwargs = {'email__iexact': identity} if is_email else {'phone_number': identity}
        user = User.objects.filter(**filter_kwargs).first()
        action = "login"
        message = ".ورود با موفقیت انجام شد"
        logger.info(f"User logged in: {user.id}")
    
    return user, action, message


def generate_tokens_for_user(user: Any) -> dict[str, str]:
    """
    Generate JWT refresh and access tokens for a given user.
    """
    refresh = RefreshToken.for_user(user)
    logger.info(f"Tokens generated for user: {user.id}")
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


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
    logger.info(f"OTP Sent to {phone_number} with async Celery task for purpose '{purpose}'")

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
    if purpose == "register" or purpose == "reset_password":
        token = generate_email_token(email, purpose)
        link = f"http://localhost:8000/api/auth/verify-otp-or-link/?email={email}&token={token}&purpose={purpose}"
        subject = "لینک تایید ایمیل"
        message = f"برای ادامه عملیات ، روی لینک زیر کلیک کنید:\n\n{link}\n\nاین لینک تا ۱۵ دقیقه معتبر است"

        # Send verification link via Celery task
        send_email_task.delay(email, subject, message)
        logger.info(f"Verification link sent to {email} with async Celery task for purpose '{purpose}'")
        return link

    else:
        otp = OTPCacheService.generate_otp(email=email, purpose=purpose)
        subject = "کد تایید"
        message = f"{otp}:کد تایید شما"

        # Generate and send OTP via email
        send_email_task.delay(email, subject, message)
        logger.info(f"OTP Sent to {email} with async Celery task for purpose '{purpose}'")
        return otp