import logging
from celery import shared_task
from django.utils.timezone import now
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

logger = logging.getLogger(__name__)

@shared_task
def cleanup_expired_tokens():
    # Delete all expired tokens (including automatically related BlacklistedToken)
    deleted_count, _ = OutstandingToken.objects.filter(expires_at__lt=now()).delete()
    logger.info(f"Cleaned up {deleted_count} expired tokens and associated blacklisted entries.")