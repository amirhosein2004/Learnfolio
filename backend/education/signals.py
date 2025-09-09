from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Video, Package


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    """
    Updates the package's popularity score when a video is saved.
    """
    package = instance.package
    
    package.popularity_score = package.popularity_score_economic
    package.save(update_fields=['popularity_score'])


@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    """
    Updates the package's popularity score when a video is deleted.
    """
    package = instance.package
    
    package.popularity_score = package.popularity_score_economic
    package.save(update_fields=['popularity_score'])
