from django.db import models
from accounts.models import AdminProfile
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField


class Blog(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True, allow_unicode=True)
    content = RichTextUploadingField()
    image = models.ImageField(upload_to='blog_covers/', blank=True, null=True)
    author = models.ForeignKey(AdminProfile, on_delete=models.SET_NULL, related_name='blogs', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
           self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
