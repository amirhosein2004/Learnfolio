from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db import models

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
            return user
        return None