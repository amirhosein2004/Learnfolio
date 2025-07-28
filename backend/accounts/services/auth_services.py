import logging
from typing import Any

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework_simplejwt.tokens import RefreshToken

from accounts.utils.communication import send_otp_for_phone, send_auth_email

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
    user = None
    if '@' in identity:
        user = User.objects.filter(email__iexact=identity).first()
    else:
        user = User.objects.filter(phone_number=identity).first()

    if user:
        # Existing user → send login OTP or email
        if '@' in identity:
            send_auth_email(email=identity, purpose='login', send_link=False)
            logger.info(f"Login OTP sent to {identity}")
            return ".کد ورود به ایمیل شما ارسال شد", 'login', reverse('accounts:verify_otp')
        else:
            send_otp_for_phone(phone_number=identity, purpose='login')
            logger.info(f"Login OTP sent to {identity}")
            return ".کد ورود برای شماره شما ارسال شد", 'login', reverse('accounts:verify_otp')
    else:
        # New user → send registration OTP or confirmation link
        if '@' in identity:
            send_auth_email(email=identity, purpose='register', send_link=True)
            logger.info(f"Registration link sent to {identity}")
            return ".لینک ثبت‌نام به ایمیل شما ارسال شد", 'register', reverse('accounts:verify_link')
        else:
            send_otp_for_phone(phone_number=identity, purpose='register')
            logger.info(f"Registration OTP sent to {identity}")
            return ".کد ثبت‌نام برای شماره شما ارسال شد", 'register', reverse('accounts:verify_otp')
        
def handle_otp_verification(identity: str, otp_obj: Any) -> tuple[User, str, str]:
    # TODO: بعدا برای تایید هم اضافه میکنیم
    """
    Verifies OTP and logs in or registers the user based on identity.

    Returns:
        tuple: (User instance, action: 'login' or 'register', message)
    """
    is_email = '@' in identity

    user = (
        User.objects.filter(email=identity).first()
        if is_email
        else User.objects.filter(phone_number=identity).first()
    )

    if not user:
        user = User.objects.create_user(phone_number=identity)
        action = "register"
        message = ".ثبت نام با موفقیت انجام شد"
        logger.info(f"User registered: {user.id}")
    else:
        action = "login"
        message = ".ورود با موفقیت انجام شد"
        logger.info(f"User logged in: {user.id}")

    otp_obj.delete()  # delete otp
    return user, action, message

def handle_link_verification(identity: str) -> tuple[User, str, str]:
    # TODO: بعدا برای تایید هم اضافه میکنیم
    """
    Registers a new user using email link verification.

    Returns:
        tuple: (User instance, action: 'register', message)
    """
    user = User.objects.create_user(email=identity)
    action = "register"
    message = ".لینک با موفقیت تایید شد"
    logger.info(f"User registered: {user.id}")
    return user, action, message

def generate_tokens_for_user(user: Any) -> dict[str, str]:
    """
    Generate JWT refresh and access tokens for a given user.

    Args:
        user (User): The user instance for whom to generate tokens.

    Returns:
        dict: A dictionary containing 'refresh' and 'access' tokens as strings.
    """
    refresh = RefreshToken.for_user(user)
    logger.info(f"Tokens generated for user: {user.id}")
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }