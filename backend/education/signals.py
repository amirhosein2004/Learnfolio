from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Video, Package
from .utils.video import calculate_package_total_duration


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    """
    Updates the package's popularity score and total duration when a video is saved.
    """
    package = instance.package
    
    # Update total duration
    total_duration = calculate_package_total_duration(package)
    package.total_duration = total_duration
    
    # Update popularity score
    package.popularity_score = package.popularity_score_economic
    package.save(update_fields=['popularity_score', 'total_duration'])


@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    """
    Updates the package's popularity score and total duration when a video is deleted.
    """
    package = instance.package
    
    # Update total duration
    total_duration = calculate_package_total_duration(package)
    package.total_duration = total_duration
    
    # Update popularity score
    package.popularity_score = package.popularity_score_economic
    package.save(update_fields=['popularity_score', 'total_duration'])
