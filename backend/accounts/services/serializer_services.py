from accounts.models import OTP
from django.core.cache import cache
from accounts.utils import verify_email_token

def get_valid_otp(identity: str, code: str): 
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

def get_resend_cache_key(identity):
    """
    Generate a cache key for resend cooldown tracking based on the user's identity
    (email or phone number).
    """
    return f"resend_{identity}"

def can_resend(identity):
    """
    Check if a resend (OTP or confirmation link) is allowed for the given identity.
    
    Returns:
        (bool, int): 
            - True if resend is allowed, False otherwise.
            - Seconds remaining until next allowed resend.
    """
    cache_key = get_resend_cache_key(identity)
    seconds_left = cache.ttl(cache_key)
    if seconds_left and seconds_left > 0:
        return False, seconds_left
    return True, 0

def set_resend_cooldown(identity, timeout):
    """
    Set a cooldown period for resending OTP or confirmation link.
    
    Args:
        identity (str): The target identifier (email or phone).
        timeout (int): Cooldown time in seconds.
    """
    cache_key = get_resend_cache_key(identity)
    cache.set(cache_key, True, timeout=timeout)

def verify_email_link(token: str):
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