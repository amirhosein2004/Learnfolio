from accounts.models import OTP

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
