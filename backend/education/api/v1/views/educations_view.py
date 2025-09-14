import logging
import os
from urllib.parse import quote
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from education.models import Package, Video
from education.api.v1.serializers.educations_serializers import (
    PackageSerializer, VideoSerializer,
    PackageListSerializer, VideoListSerializer
)
from core.permissions import UserAdminOrReadOnly, VideoPermission
from core.pagination import PackagePagination, VideoPagination
from rest_framework.exceptions import ValidationError, NotFound
from django.http import Http404, HttpResponse, FileResponse
from django.core.files.storage import default_storage


logger = logging.getLogger(__name__)


class PackageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for package management with filtering options:
    - newest: newest packages
    - most_viewed: most viewed packages
    - most_popular: most popular packages based on popularity_score
    """
    queryset = Package.objects.filter(is_active=True)
    permission_classes = [UserAdminOrReadOnly]
    pagination_class = PackagePagination
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    filterset_fields = ['is_free']
    ordering_fields = ['-created_at', 'view_count', 'popularity_score']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return PackageListSerializer
        return PackageSerializer
    
    def perform_create(self, serializer):
        """
        Save the package with the admin profile of the current user.
        """
        serializer.save(author=self.request.user.admin_profile)

    def perform_update(self, serializer):
        """
        Update the package with the admin profile of the current user.
        """
        serializer.save(author=serializer.instance.author)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a package and increment view count
        """
        instance = self.get_object()
        if not request.user.is_staff:
            instance.increment_view_count()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """
        Create a new package.
        """
        try:
            response = super().create(request, *args, **kwargs)
            return Response({'message': '.پکیج با موفقیت ایجاد شد', 'data': response.data}, status=201)
        except ValidationError as e:
            return Response(e.detail, status=400)
        except Exception:
            logger.error("Error creating package", exc_info=True)
            return Response({'detail': ".خطای ناشناخته ای رخ داده است لطفا دوباره تلاش کنید"}, status=500)

    def update(self, request, *args, **kwargs):
        """
        Update an existing package.
        """
        try:
            response = super().update(request, *args, **kwargs)
            return Response({'message': '.پکیج با موفقیت ویرایش شد', 'data': response.data}, status=200)
        except ValidationError as e:
            return Response(e.detail, status=400)
        except (NotFound, Http404):
            return Response({'detail': '.پکیج مورد نظر یافت نشد'}, status=404)
        except Exception:
            logger.error("Error updating package", exc_info=True)
            return Response({'detail': ".خطای ناشناخته ای رخ داده است لطفا دوباره تلاش کنید"}, status=500)

    def destroy(self, request, *args, **kwargs):
        """
        Delete an existing package.
        """
        try:
            super().destroy(request, *args, **kwargs)
            return Response({'message': '.پکیج با موفقیت حذف شد'}, status=204)
        except ValidationError as e:
            return Response(e.detail, status=400)
        except (NotFound, Http404):
            return Response({'detail': '.پکیج مورد نظر یافت نشد'}, status=404)
        except Exception:
            logger.error("Error deleting package", exc_info=True)
            return Response({'detail': ".خطای ناشناخته ای رخ داده است لطفا دوباره تلاش کنید"}, status=500)


class VideoViewSet(viewsets.ModelViewSet):
    """
    API endpoint for video management within packages
    """
    queryset = Video.objects.all()
    permission_classes = [VideoPermission]
    pagination_class = VideoPagination
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'list':
            return VideoListSerializer
        return VideoSerializer

    def get_queryset(self):
        package_slug = self.kwargs.get("package_slug")
        return Video.objects.select_related('package').filter(package__slug=package_slug)
    
    @action(detail=False, methods=['post'], url_path='reorder')
    def reorder(self, request, package_slug=None):
        """
        Reorder videos 
        """
        try:
            new_order = request.data.get("order", [])
            
            videos_to_update = []
            queryset = self.get_queryset()
            
            for index, video_id in enumerate(new_order):
                try:
                    video = queryset.get(id=video_id)
                    video.order = index
                    videos_to_update.append(video)
                except Video.DoesNotExist:
                    continue

            if videos_to_update:
                Video.objects.bulk_update(videos_to_update, ['order'])
            
            return Response({'message': 'ترتیب ویدیوها با موفقیت تغییر کرد'}, status=200)
        except Exception as e:
            logger.error(f"Error reordering videos: {e}", exc_info=True)
            return Response({'detail': 'خطا در تغییر ترتیب ویدیوها'}, status=500)

    @action(detail=True, methods=['get'], url_path='download')
    def download(self, request, slug=None, package_slug=None):
        """
        Simplified video download - works for both local and cloud storage
            """
        try:
            video = self.get_object()
            if not video.video_file or not default_storage.exists(video.video_file.name):
                return Response({'detail': 'فایل ویدیو یافت نشد'}, status=404)

            video.increment_download_count()
            file_name = os.path.basename(video.video_file.name)
            file_path = getattr(video.video_file, 'path', None)

            try:
                if file_path and os.path.exists(file_path):
                    # local file
                    response = FileResponse(
                        open(file_path, 'rb'),
                        content_type='application/octet-stream'
                    )
                else:
                    # cloud file
                    with default_storage.open(video.video_file.name, 'rb') as f:
                        response = HttpResponse(f.read(), content_type='application/octet-stream')

                response['Content-Disposition'] = f'attachment; filename="{quote(file_name)}"'
                return response 

            except Exception as e:
                logger.error(f"Error serving file: {e}", exc_info=True)
                return Response({'detail': 'خطا در دانلود فایل'}, status=500)
                
        except Video.DoesNotExist:
            return Response({'detail': 'ویدیو مورد نظر یافت نشد'}, status=404)
        except Exception as e:
            logger.error(f"Error in download method: {e}", exc_info=True)
            return Response({'detail': 'خطای ناشناخته در دانلود فایل'}, status=500)
    
    def create(self, request, *args, **kwargs):
        """
        Create a new video.
        """
        try:
            response = super().create(request, *args, **kwargs)
            return Response({'message': '.ویدیو با موفقیت ایجاد شد', 'data': response.data}, status=201)
        except ValidationError as e:
            return Response(e.detail, status=400)
        except Exception:
            logger.error("Error creating video", exc_info=True)
            return Response({'detail': ".خطای ناشناخته ای رخ داده است لطفا دوباره تلاش کنید"}, status=500)
    
    def update(self, request, *args, **kwargs):
        """
        Update an existing video.
        """
        try:
            response = super().update(request, *args, **kwargs)
            return Response({'message': '.ویدیو با موفقیت ویرایش شد', 'data': response.data}, status=200)
        except ValidationError as e:
            return Response(e.detail, status=400)
        except (NotFound, Http404):
            return Response({'detail': '.ویدیو مورد نظر یافت نشد'}, status=404)
        except Exception:
            logger.error("Error updating video", exc_info=True)
            return Response({'detail': ".خطای ناشناخته ای رخ داده است لطفا دوباره تلاش کنید"}, status=500)
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete an existing video.
        """
        try:
            super().destroy(request, *args, **kwargs)
            return Response({'message': '.ویدیو با موفقیت حذف شد'}, status=204)
        except ValidationError as e:
            return Response(e.detail, status=400)
        except (NotFound, Http404):
            return Response({'detail': '.ویدیو مورد نظر یافت نشد'}, status=404)
        except Exception:
            logger.error("Error deleting video", exc_info=True)
            return Response({'detail': ".خطای ناشناخته‌ای رخ داده است لطفا دوباره تلاش کنید"}, status=500)
