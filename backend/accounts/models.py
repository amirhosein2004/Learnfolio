from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import UserManager

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