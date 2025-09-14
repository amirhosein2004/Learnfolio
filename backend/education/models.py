import math
from django.db import models
from django.db.models import F
from django.utils.text import slugify
from ordered_model.models import OrderedModel
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from accounts.models import AdminProfile


User = get_user_model()


class Package(models.Model):
    """
    Educational Package Model
    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True, allow_unicode=True)
    description = RichTextUploadingField()
    status = models.CharField(max_length=20, choices=[
        ('completed', 'اتمام'),
        ('recording', 'در حال ضبط'),
        ('soon', 'بزودی')
    ])

    thumbnail = models.ImageField(upload_to='packages/thumbnails/')
    is_free = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    total_duration = models.PositiveIntegerField(null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    popularity_score = models.FloatField(default=0.0) 
    
    author = models.ForeignKey(AdminProfile, on_delete=models.SET_NULL, null=True, related_name='packages')
    download_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_active', '-created_at']),
            models.Index(fields=['is_free']),
            models.Index(fields=['-view_count']),
            models.Index(fields=['-popularity_score']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def increment_view_count(self):
        """increase view count"""
        Package.objects.filter(pk=self.pk).update(view_count=F('view_count') + 1)
        # self.refresh_from_db(fields=['view_count'])

    @property
    def popularity_score_economic(self):
        """calculate popularity score using economic formula"""
        views = self.view_count if self.view_count is not None else 1
        duration = self.total_duration if self.total_duration is not None else 1
        price = self.price or 0

        if self.is_free or price <= 0:
            price_factor = 0
        else:
            price_factor = 0.2 * math.log(price + 1)

        score = (views ** 0.6) * ((1 + math.log(duration + 1)) ** 0.3) * (1 + price_factor)
        return round(score, 2)


def video_upload_to(instance, filename):
    """
    Upload video file to a specific directory based on package title
    """
    return f"videos/{instance.package.title}/{filename}"

class Video(OrderedModel):
    """
    Video Model
    """
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, blank=True, allow_unicode=True)
    description = RichTextUploadingField(null=True, blank=True)
    video_file = models.FileField(upload_to=video_upload_to)
    
    is_free = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # videos order by package
    order_with_respect_to = 'package'
    
    class Meta:
        ordering = ['order']
        unique_together = ['package', 'slug', 'title']
        indexes = [
            models.Index(fields=['package']),
            models.Index(fields=['is_free']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.package.title} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        if self.package.is_free:
            self.is_free = True
        super().save(*args, **kwargs)
    
    def increment_download_count(self):
        """increase number of download package"""
        Package.objects.filter(pk=self.package_id).update(download_count=F('download_count') + 1)
        # self.package.refresh_from_db(fields=['download_count'])


class UserPackage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchased_packages')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='purchasers')
    price_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    purchased_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'package')
        indexes = [
            models.Index(fields=['user', 'package']),
        ]

    def __str__(self):
        return f"{self.user.username} → {self.package.title}"


# NOTE: for later that we can add variants to videos
# def variant_upload_to(instance, filename):
#     """
#     مسیر ذخیره سازی بر اساس id ویدیو اصلی
#     """
#     return f"videos/variants/{instance.video.id}/{instance.quality}/"

# class VideoVariant(models.Model):
#     QUALITY_CHOICES = [
#         ("240p", "240p"),
#         ("480p", "480p"),
#         ("720p", "720p"),
#         ("1080p", "1080p"),
#         ("hls", "HLS Stream"),
#     ]
    
#     video = models.ForeignKey(Video, related_name="variants", on_delete=models.CASCADE)
#     quality = models.CharField(max_length=20, choices=QUALITY_CHOICES)
#     file_url = models.FileField(upload_to=variant_upload_to)
