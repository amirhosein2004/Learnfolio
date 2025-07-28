from typing import Optional, Union
from accounts.models import OTP
from accounts.utils.token_utils import verify_email_token
from django.contrib.auth import get_user_model

User = get_user_model()

def get_valid_otp(identity: str, code: str) -> tuple[OTP, str]: 
    """
    Validate OTP for given identity and code.
    Returns (otp, error_message) tuple.
    If otp is valid, error_message will be None.
    """

    filters = {"code": code}
    if "@" in identity:
        filters["email"] = identity
    else:
        filters["phone_number"] = identity

    otp = OTP.objects.filter(**filters).order_by("-created_at").first()

    if not otp or otp.is_expired():
        return None, ".کد وارد شده اشتباه یا منقضی شده است. لطفاً دوباره تلاش کنید"

    return otp, None

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