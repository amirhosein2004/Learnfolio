from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import UserManager, OTPManager
from django.contrib.auth import get_user_model
from django.utils import timezone
import secrets

User = get_user_model()

# ---------------------
# Custom User Model
# ---------------------
class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)

    is_active = models.BooleanField(default=True) 
    is_staff = models.BooleanField(default=False) # Admin site access
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = UserManager() # custom UserManager to handle user creation

    # USERNAME_FIELD specifies the unique identifier for authentication.
    # Here, it's set to 'phone_number', but custom authentication can also handle 'email'.
    USERNAME_FIELD = 'phone_number' 
    REQUIRED_FIELDS = [] # REQUIRED_FIELDS for superuser

    def __str__(self):
        return self.email or self.phone_number or "User"
    
# ---------------------
# Admin Profile(owner site)
# ---------------------
class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile') # One-to-one link to the custom user model
    social_networks = models.JSONField(default=dict, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Admin: {self.user.full_name}"

# ---------------------
# OTP Code
# ---------------------
class OTP(models.Model):
    """
    Model to store One-Time Passwords (OTPs) for user authentication purposes,
    including login, registration, and password reset.
    """
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    code = models.CharField(max_length=6)
    purpose = models.CharField(max_length=20, choices=[
        ('login', 'Login'),
        ('register', 'Register'),
        ('reset', 'Reset Password'),
    ]) # The context in which the OTP is used

    created_at = models.DateTimeField(auto_now_add=True)

    objects = OTPManager() # OTP Manager

    class Meta:
        indexes = [
            models.Index(fields=['email', 'phone_number', 'code']), # Index for faster lookup
        ]

    def __str__(self):
        return f"{self.purpose} - {self.email or self.phone_number} - {self.code}"

    #  Check if the OTP has expired.(Return bool)
    def is_expired(self, expire_minutes=2):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=expire_minutes)

    def regenerate(self):
        """
        Regenerate the OTP code and update the timestamp.

        Typically used when a user requests to resend the OTP code.
        """
        self.code = str(secrets.randbelow(1000000)).zfill(6)
        self.created_at = timezone.now()
        self.save()