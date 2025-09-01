from django.conf import settings
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

def generate_email_token(email: str, purpose: str) -> str:
    """
    Generate a secure token for email verification purposes.
    Args:
        email (str): The user's email address.
        purpose (str): The purpose of the token (e.g., 'register', 'reset').
    Returns:
        str: The generated token as a string.
    """
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    return serializer.dumps({'email': email, 'purpose': purpose})


def verify_email_token(token: str, max_age: int = 900) -> tuple[dict | None, str | None]:
    """
    Verify the given token and return the stored data (email and purpose).
    Args:
        token (str): The token to verify.
        max_age (int): Maximum age of the token in seconds (default: 900, 15 minutes).
    Returns:
        - The stored data as a dictionary if the token is valid.
        - An error message if the token is invalid.
    """
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        data = serializer.loads(token, max_age=max_age)
        return data, None  # None means no error
    except SignatureExpired:
        return None, "توکن منقضی شده است. لطفاً مجدداً درخواست دهید."
    except BadSignature:
        return None, "توکن نامعتبر است." # None means no data
    except Exception as e:
        return None, f"خطای نامشخص در اعتبارسنجی توکن: {e}"