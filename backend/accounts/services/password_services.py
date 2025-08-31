import logging
from django.contrib.auth import get_user_model
from accounts.services.validation_services import get_identity_purpose
from accounts.services.auth_services import send_otp_for_phone, send_auth_email
from django.urls import reverse
import jwt
import datetime
from django.conf import settings

logger = logging.getLogger(__name__)

User = get_user_model()

def handle_password_reset(identity: str) -> tuple[str, str, str]:
    """
    Send OTP or confirmation link for password reset
    - if user exists send OTP or confirmation link
    - if user not exists do nothing and return message
    Returns:
        tuple: (Result message, purpose, Next step URL)
    """
    purpose = get_identity_purpose(identity, context="reset_password")
    is_email = '@' in identity
    
    if is_email:
        user_exists = User.objects.filter(email__iexact=identity).exists()
        if user_exists:
            send_auth_email(email=identity, purpose=purpose)
            logger.info(f"Password reset link sent to {identity}")
        else: # we dont say user does not exist because security reasons
            logger.info(f"Password reset attempted for non-existent email {identity}")
        return "لینک تایید به ایمیل ارسال شد", purpose, reverse('accounts_v1:password_verify_link')
    else:
        user_exists = User.objects.filter(phone_number=identity).exists()
        if user_exists:
            send_otp_for_phone(phone_number=identity, purpose=purpose)
            logger.info(f"Password reset OTP sent to {identity}")
        else: # we dont say user does not exist because security reasons
            logger.info(f"Password reset attempted for non-existent phone {identity}")
        return "کد تایید به شماره تلفن ارسال شد", purpose, reverse('accounts_v1:password_verify_otp')

def change_user_password(user: User, new_password: str):
    """change user password"""
    user.set_password(new_password)
    logger.info(f"Password changed for user {user}")
    user.save()

def generate_reset_password_token(identity: str) -> str:
    """
    generate token for reset password with information like identity ...
    """
    payload = {
        "identity": identity,
        "type": "reset_password",
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30),
        "iat": datetime.datetime.now(datetime.timezone.utc),
    }
    logger.info(f"Reset password token generated for {identity}")
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

def get_user_by_identity(identity: str) -> User:
    """
    get user by identity
    """
    if '@' in identity:
        user = User.objects.get(email=identity)
    else:
        user = User.objects.get(phone_number=identity)
    return user