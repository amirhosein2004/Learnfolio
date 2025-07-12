from celery import shared_task
from django.utils import timezone
from accounts.models import OTP
from datetime import timedelta


@shared_task
def delete_expired_otps(expire_minutes=2):
    """
    Delete OTPs older than `expire_minutes` (default 2 minutes).
    """
    threshold = timezone.now() - timedelta(minutes=expire_minutes)
    expired_qs = OTP.objects.filter(created_at__lt=threshold)
    # count = expired_qs.count()
    expired_qs.delete()
    # logger.info(f"[Celery Beat] Deleted {count} expired OTPs older than {expire_minutes} minutes.")
