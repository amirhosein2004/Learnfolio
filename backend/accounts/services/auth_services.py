from django.contrib.auth import get_user_model
from accounts.utils import send_otp_for_phone, send_auth_email

User = get_user_model()

def handle_identity_submission(identity: str) -> str:
    """
    Sends an OTP or a confirmation link based on the user's identity.

    - If the user exists: send login code (email or phone).
    - If not: send signup link (email) or code (phone).

    Args:
        identity (str): Email or phone number.

    Returns:
        str: Result message.
    """
    user = None
    if '@' in identity:
        user = User.objects.filter(email__iexact=identity).first()
    else:
        user = User.objects.filter(phone_number=identity).first()

    if user:
        # Existing user → send login OTP or email
        if '@' in identity:
            send_auth_email(email=identity, purpose='login', send_link=False)
            return ".کد ورود به ایمیل شما ارسال شد"
        else:
            send_otp_for_phone(phone_number=identity, purpose='login')
            return ".کد ورود برای شماره شما ارسال شد"
    else:
        # New user → send registration OTP or confirmation link
        if '@' in identity:
            send_auth_email(email=identity, purpose='register', send_link=True)
            return ".لینک ثبت‌نام به ایمیل شما ارسال شد"
        else:
            send_otp_for_phone(phone_number=identity, purpose='register')
            return ".کد ثبت‌نام برای شماره شما ارسال شد"
