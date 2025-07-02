from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from django.db import models
import secrets

# ---------------------
# Custom User Manager
# ---------------------
class UserManager(BaseUserManager):
    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        """
        Creates and returns a regular user with either email or phone number.
        If neither is provided, raises a ValueError.
        """
        if not email and not phone_number:
            raise ValueError("Either email or phone number is required.")

        # Normalize email if provided
        email = self.normalize_email(email) if email else None

        # Create user instance
        user = self.model(
            email=email,
            phone_number=phone_number,
            **extra_fields
        )

        # Set password if provided; otherwise mark as unusable
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, phone_number=None, password=None, **extra_fields):
        """
        Creates and returns a superuser with is_staff and is_superuser set to True.
        Accepts either email or phone number.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(
            email=email,
            phone_number=phone_number,
            password=password,
            **extra_fields
        )

# ---------------------
# Custom OTP Manager
# --------------------- 
class OTPManager(models.Manager):
    """
    Manager to generate a new OTP for a user by removing any existing OTPs.
    Ensures only one active OTP per user regardless of purpose.
    """

    def generate_otp(self, email=None, phone_number=None, purpose=None):
        """
        Deletes any existing OTPs for the given user and creates a new one.

        Args:
            email (str, optional): User's email address.
            phone_number (str, optional): User's phone number.
            purpose (str): The OTP usage context (e.g., login, reset).

        Returns:
            tuple: (new OTP instance, True)
        """
        filters = {
            "email": email,
            "phone_number": phone_number,
        }

        # Delete all existing OTPs for the user
        self.filter(**filters).delete()

        # Create and return a new OTP
        return self.create(
            code=str(secrets.randbelow(1000000)).zfill(6),
            purpose=purpose,
            **filters
        ), True