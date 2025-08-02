import logging
from django.contrib.auth.models import BaseUserManager

logger = logging.getLogger(__name__)

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
        logger.info(f"User created. Email: {email}, Phone: {phone_number}, Has password: {bool(password)}")
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