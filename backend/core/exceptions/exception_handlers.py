from rest_framework.views import exception_handler
from rest_framework.exceptions import Throttled
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF.
    """
    if isinstance(exc, Throttled):
        # Return a custom response for throttling (rate limit) errors
        custom_response_data = {
            'detail': '.شما بیش از حد مجاز درخواست ارسال کرده‌اید. لطفاً بعداً تلاش کنید',
            'available_in_seconds': exc.wait,
        }
        return Response(custom_response_data, status=429)

    # Use DRF's default exception handler for other errors
    response = exception_handler(exc, context)
    return response
