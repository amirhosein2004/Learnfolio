import logging
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db import models

logger = logging.getLogger(__name__)

User = get_user_model()

class EmailOrPhoneBackend(ModelBackend):
    """
    Authenticate with either email or phone_number + password.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        # trying to find the user by email or number.
        user = User.objects.filter(
            models.Q(email__iexact=username) | 
            models.Q(phone_number__iexact=username)
        ).first()

        # If the user was found and the password was correct, return it.
        if user and user.check_password(password):
            logger.info(f"Authentication success for user: {username}")
            return user
        logger.warning(f"Authentication failed for user: {username}")
        return None