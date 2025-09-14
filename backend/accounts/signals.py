from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, AdminProfile


@receiver(post_save, sender=User)
def ensure_admin_profile(sender, instance, created, **kwargs):
    """
    Ensure that an AdminProfile exists whenever a User with is_staff=True is created or updated.
    """
    if instance.is_staff and not hasattr(instance, 'admin_profile'):
        AdminProfile.objects.create(user=instance)
