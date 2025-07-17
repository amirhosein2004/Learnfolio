'''فعلا همینجا میزاریم درون دایرکتوری utils تا بعدا اگر به بحث های امنیتی بیشتری نیاز پیدا کردیم در دایرکتوری security'''
import requests
from django.conf import settings

def verify_turnstile_token(token: str = None, remoteip=None) -> bool:
    """
    Returns True if CAPTCHA is disabled or token is valid.
    Returns False if CAPTCHA is enabled and token is missing or invalid.
    """
    if not settings.TURNSTILE_ENABLED:
        return True  # CAPTCHA is disabled globally

    if not token:
        return False  # CAPTCHA is enabled, but no token sent

    data = {
        'secret': settings.TURNSTILE_SECRET_KEY,
        'response': token,
    }
    if remoteip:
        data['remoteip'] = remoteip

    try:
        # Send POST request to Cloudflare Turnstile verification endpoint
        resp = requests.post(
            'https://challenges.cloudflare.com/turnstile/v0/siteverify',
            data=data,
            timeout=5
        )
        result = resp.json()
        return result.get("success", False)
    except Exception:
        return False
