import math
from django.db import models
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
    
    @property
    def increment_view_count(self):
        """increase view count"""
        self.view_count += 1
        self.save(update_fields=['view_count'])

    @property
    def popularity_score_economic(self):
        """calculate popularity score using economic formula"""
        views = max(self.view_count, 1)
        duration = max(self.total_duration, 1)
        price = self.price or 0

        if self.is_free or price <= 0:
            price_factor = 0
        else:
            price_factor = 0.2 * math.log(price + 1)

        score = (views ** 0.6) * ((1 + math.log(duration + 1)) ** 0.3) * (1 + price_factor)
        return round(score, 2)

    @property
    def calculate_total_download(self):
        """calculate total download count"""
        return self.videos.aggregate(total=Sum('download_count'))['total']


class Video(OrderedModel):
    """
    Video Model
    """
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True, allow_unicode=True)
    description = RichTextUploadingField()
    video_file = models.FileField(upload_to='videos/')
    
    is_free = models.BooleanField(default=False)
    download_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    order_with_respect_to = 'package'
    
    class Meta:
        ordering = ['order']
        unique_together = ['package', 'slug']
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
        super().save(*args, **kwargs)
    
    @property
    def increment_download_count(self):
        """increase number of download"""
        self.download_count += 1
        self.save(update_fields=['download_count'])


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
