import logging
from typing import Any

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework_simplejwt.tokens import RefreshToken

from accounts.utils.communication import send_otp_for_phone, send_auth_email
from accounts.services.validation_services import get_otp_purpose

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
    purpose = get_otp_purpose(identity)

    if '@' in identity:
        if purpose == "register":
            # For registration, send confirmation link
            send_auth_email(email=identity, purpose=purpose)
            logger.info(f"Registration link sent to {identity}")
            return ".لینک ثبت‌نام به ایمیل شما ارسال شد", purpose, reverse('accounts:verify_link')

        else:
            otp_code = send_auth_email(email=identity, purpose=purpose)
            logger.info(f"Login OTP sent to {identity}")
            return ".کد تایید به ایمیل شما ارسال شد", purpose, reverse('accounts:verify_otp')
            
    else:
        otp_code = send_otp_for_phone(phone_number=identity, purpose=purpose)
        logger.info(f"OTP sent to phone {identity}")
        return f".کد تایید به شماره تلفن شما ارسال شد: {otp_code}", purpose, reverse('accounts:verify_otp')

def login_or_register_user(identity: str) -> tuple[User, str, str]:
    """
    Log in or register a user based on their identity (email or phone number).
    Args:
        identity (str): The user's email or phone number.
    Returns:
        tuple: (User instance, action performed, success message)
    """
    purpose = get_otp_purpose(identity)
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