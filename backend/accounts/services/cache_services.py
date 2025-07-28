from django.core.cache import cache

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