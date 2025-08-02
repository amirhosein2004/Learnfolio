from django.core.cache import cache
import secrets
import logging

logger = logging.getLogger(__name__)

class OTPCacheService:
    """
    Service class for generating and storing OTP codes in cache.
    Used for identity verification (e.g., login, registration, reset paasword).
    """
    OTP_TTL = 2 * 60  # 2 minutes in seconds

    @staticmethod
    def _make_key(email=None, phone_number=None, purpose=None):
        """
        Generates a unique cache key for the given identity and purpose.
        """
        identity = email or phone_number
        return f"otp:{identity}:{purpose}"

    @classmethod
    def generate_otp(cls, email=None, phone_number=None, purpose="login"):
        """
        Generates a 6-digit OTP, stores it in cache for a limited time, and returns it.
        Args:
            email (str): User's email address (optional)
            phone_number (str): User's phone number (optional)
            purpose (str): OTP purpose (e.g., "login", "register")
        Returns:
            str: The generated OTP code
        """
        otp = str(secrets.randbelow(1000000)).zfill(6)
        key = cls._make_key(email, phone_number, purpose)
        cache.set(key, otp, timeout=cls.OTP_TTL)
        logger.info(f"Generated OTP for {email or phone_number} (purpose: {purpose})")
        return otp

def get_resend_cache_key(identity: str) -> str:
    """
    Generate a cache key for resend cooldown tracking based on the user's identity
    (email or phone number).
    """
    return f"resend_{identity}"

def can_resend(identity: str) -> tuple[bool, int]:
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

def set_resend_cooldown(identity: str, timeout: int = 300) -> None:
    """
    Set a cooldown period for resending OTP or confirmation link.
    
    Args:
        identity (str): The target identifier (email or phone).
        timeout (int): Cooldown time in seconds.
    """
    cache_key = get_resend_cache_key(identity)
    cache.set(cache_key, True, timeout=timeout)