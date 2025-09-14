from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin
from education.models import Package, Video


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'is_free', 'price', 'total_duration', 'view_count', 'created_at']
    list_filter = ['status', 'is_free', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Video)
class VideoAdmin(OrderedModelAdmin):
    list_display = ['title', 'package', 'is_free', 'move_up_down_links']
    list_filter = ['is_free', 'package', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['package', 'order']
