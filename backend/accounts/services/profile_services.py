import logging
from accounts.services.auth_services import send_otp_for_phone, send_auth_email
from accounts.services.auth_services import get_identity_purpose
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

logger = logging.getLogger(__name__)


def handle_identity_update(identity: str) -> tuple[str, str, str]:
    """
    Sends an OTP or a confirmation link based on the user's identity.

    - If the identity is email: send confirmation link
    - If the identity is phone: send OTP code 

    Returns:
        tuple: (Result message,purpose,next step url)
    """
    purpose = get_identity_purpose(identity, context="update_identity")

    if '@' in identity:
        send_auth_email(email=identity, purpose=purpose)
        logger.info(f"for Identity update link sent to {identity}")
        return "لینک تایید به ایمیل ارسال شد", purpose, reverse('accounts_v1:user_update_email_confirm')
    else:
        send_otp_for_phone(phone_number=identity, purpose=purpose)
        logger.info(f"for Identity update OTP sent to {identity}")
        return "کد تایید به شماره تلفن ارسال شد", purpose, reverse('accounts_v1:user_update_phone_verify')


def delete_user_account(user: User) -> bool: 
    user_id = user.id

    user.delete()

    logger.info(f"User account {user_id} successfully deleted")
    return True
