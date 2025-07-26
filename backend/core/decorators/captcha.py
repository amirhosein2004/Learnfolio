from rest_framework.response import Response
from rest_framework import status
from functools import wraps
from core.utils.network import get_client_ip
from core.utils.captcha import verify_turnstile_token
import logging

logger = logging.getLogger(__name__)

def captcha_required(view_func):
    """
    Decorator to validate Turnstile CAPTCHA before executing a view.

    Checks "cf-turnstile-response" in request data. If invalid or missing, logs the client's IP and returns 400.
    Otherwise, proceeds with the original view.
    """
    @wraps(view_func)
    def _wrapped_view(self, request, *args, **kwargs):
        captcha_token = request.data.get("cf-turnstile-response")
        remote_ip = get_client_ip(request)

        if not verify_turnstile_token(captcha_token, remoteip=remote_ip):
            logger.warning(f"[CAPTCHA FAILED] IP: {remote_ip}")
            return Response(
                {"detail": ".اعتبارسنجی کپچا ناموفق بود"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return view_func(self, request, *args, **kwargs)

    return _wrapped_view
