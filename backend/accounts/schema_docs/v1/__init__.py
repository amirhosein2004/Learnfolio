from .auth.submit_identity import identity_submit_schema
from .auth.verify_otp import otp_verification_schema
from .auth.verify_link import link_verification_schema
from .auth.login_password import password_login_schema
from .auth.logout import logout_schema


from .password.first_time_password import first_time_password_schema
from .password.change_password import change_password_schema
from .password.reset_password import reset_password_schema
from .password.link_verification_password_reset import link_verification_password_reset_schema
from .password.otp_verification_password_reset import otp_verification_password_reset_schema
from .password.request_password_reset import request_password_reset_schema


from .profile.admin_profile import admin_profile_get_schema, admin_profile_patch_schema
from .profile.user_profile import user_profile_get_schema, user_profile_patch_schema, user_profile_delete_schema
from .profile.update_identity import user_update_identity_schema
from .profile.confirm_email_update import confirm_email_update_schema
from .profile.verify_phone_update import verify_otp_phone_update_schema


__all__ = [
    # auth
    "identity_submit_schema",
    "otp_verification_schema",
    "link_verification_schema",
    "password_login_schema",
    "logout_schema",
    # password
    "first_time_password_schema",
    "change_password_schema",
    "reset_password_schema",
    "link_verification_password_reset_schema",
    "otp_verification_password_reset_schema",
    "request_password_reset_schema",
    # profile
    "admin_profile_get_schema",
    "admin_profile_patch_schema",
    "user_profile_get_schema",
    "user_profile_patch_schema",
    "user_profile_delete_schema",
    "user_update_identity_schema",
    "confirm_email_update_schema",
    "verify_otp_phone_update_schema",
]
