import logging
from typing import Optional, Union, Literal
from django.core.cache import cache
from accounts.services.cache_services import OTPCacheService
from accounts.utils.token_utils import verify_email_token
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)

User = get_user_model()

def get_otp_purpose(identity: str) -> Literal["login", "register"]:
    """
    Determine purpose of OTP based on existence of user.
    Returns 'login' if user exists, else 'register'.
    """
    if '@' in identity:
        return "login" if User.objects.filter(email__iexact=identity).exists() else "register"
    return "login" if User.objects.filter(phone_number=identity).exists() else "register"

def get_valid_otp(identity: str, code: str, purpose: str) -> tuple[bool, None] | tuple[None, str]:
    """
    Validate OTP for given identity, code, and purpose using cache.

    Returns:
        (True, None) → if OTP is valid
        (None, error_message) → if invalid or expired
    """
    if "@" in identity:
        email, phone = identity, None
    else:
        email, phone = None, identity

    key = OTPCacheService._make_key(email=email, phone_number=phone, purpose=purpose)
    real_code = cache.get(key)

    if real_code is None:
        return None, ".کد منقضی شده است. لطفاً دوباره درخواست دهید"
    
    if real_code != code:
        return None, ".کد وارد شده نادرست است"

    cache.delete(key)
    return True, None

def verify_email_link(token: str) -> tuple[bool, Optional[str]]:
    """
    Verify a confirmation link token.

    Args:
        token (str): The token to verify.

    Returns:
        Tuple[bool, Optional[str]]: 
            - True if the token is valid, False otherwise.
            - An error message if the token is invalid.
    """
    data, error = verify_email_token(token) # data contain(email, purpose)
    if error:
        return False, error
    logger.info(f"Email link verified for {data['email']}")
    return True, None

def validate_user_with_password(identity: str, password: str) -> tuple[bool, Union[str, User]]:
    """
    Validate the user using email or phone number and password.
    If there's an error, returns (False, error message),
    otherwise returns (True, user).
    """
    if '@' in identity:
        user = User.objects.filter(email__iexact=identity).first()
    else:
        user = User.objects.filter(phone_number=identity).first()

    if not user: # user not exist
        return False, ".کاربر وجود ندارد یا رمز اشتباه است"

    if not user.has_usable_password(): # user password not set
        return False, ".رمز عبور اشتباه است یا هنوز تنظیم نشده است"

    if not user.check_password(password): # user password not true
        return False, ".رمز عبور اشتباه است یا هنوز تنظیم نشده است"

    return True, user