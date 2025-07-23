from django.contrib.auth import get_user_model
from accounts.utils import send_otp_for_phone, send_auth_email
from rest_framework_simplejwt.tokens import RefreshToken

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
        
def verify_otp_or_link(identity: str, otp_obj):
    """
    Verify OTP purpose and get or create user based on identity.

    - Checks if identity is email or phone number.
    - If user exists, login.
    - If user not found, create new user (register).
    - after success proccess delete otp obj 
    - Returns user instance, action type ("login" or "register"), and success message.
    """
    purpose = otp_obj.purpose
    is_email = '@' in identity

    if purpose in ["login", "register"]:
        if is_email:
            user = User.objects.filter(email=identity).first()
        else:
            user = User.objects.filter(phone_number=identity).first()

        if not user:
            # TODO: تایید ایمیل بعدا اضافه شود
            user = User.objects.create_user(email=identity) if is_email else User.objects.create_user(phone_number=identity)
            action = "register"
            message = ".ثبت نام و ورود با موفقیت انجام شد"
        else:
            action = "login"
            message = ".ورود با موفقیت انجام شد"

        otp_obj.delete()  # delete otp
        return user, action, message

def generate_tokens_for_user(user):
    """
    Generate JWT refresh and access tokens for a given user.

    Args:
        user (User): The user instance for whom to generate tokens.

    Returns:
        dict: A dictionary containing 'refresh' and 'access' tokens as strings.
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }