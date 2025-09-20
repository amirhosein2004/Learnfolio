import logging
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from education.models import Package, Video, UserPackage
from education.api.v1.serializers.educations_serializers import (
    PackageSerializer, VideoSerializer,
    PackageListSerializer, VideoListSerializer
)
from core.permissions import UserAdminOrReadOnly, VideoPermission
from core.pagination import PackagePagination, VideoPagination
from rest_framework.exceptions import ValidationError, NotFound
from django.http import Http404
from drf_spectacular.utils import extend_schema_view, extend_schema
from education.schema_docs.v1 import (
    package_list_schema,
    package_retrieve_schema,
    package_create_schema,
    package_update_schema,
    package_delete_schema,
    video_list_schema,
    video_retrieve_schema,
    video_create_schema,
    video_update_schema,
    video_delete_schema,
    video_reorder_schema,
    video_download_schema,
)
from education.services.video_service import VideoService


logger = logging.getLogger(__name__)


@extend_schema_view(
    list=extend_schema(**package_list_schema),
    retrieve=extend_schema(**package_retrieve_schema),
    create=extend_schema(**package_create_schema),
    update=extend_schema(**package_update_schema),
    partial_update=extend_schema(**package_update_schema),
    destroy=extend_schema(**package_delete_schema),
)
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

        is_access = False
        if request.user.is_authenticated:
            is_access = instance.purchasers.filter(user=request.user).exists()
            
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['is_access'] = is_access 
        
        return Response(data)
    
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


@extend_schema_view(
    list=extend_schema(**video_list_schema),
    retrieve=extend_schema(**video_retrieve_schema),
    create=extend_schema(**video_create_schema),
    update=extend_schema(**video_update_schema),
    partial_update=extend_schema(**video_update_schema),
    destroy=extend_schema(**video_delete_schema),
    reorder=extend_schema(**video_reorder_schema),
    download=extend_schema(**video_download_schema),
)
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
        new_order = request.data.get("order", [])
        queryset = self.get_queryset()
        
        success, message = VideoService.reorder_videos(queryset, new_order)
        
        if success:
            return Response({'message': message}, status=200)
        else:
            return Response({'detail': message}, status=500)

    @action(detail=True, methods=['get'], url_path='download')
    def download(self, request, slug=None, package_slug=None):
        """
        Simplified video download - works for both local and cloud storage
        """
        try:
            video = self.get_object()
            success, response_or_error = VideoService.prepare_video_download(video)
            
            if success:
                return response_or_error
            else:
                return Response({'detail': response_or_error}, status=404 if 'یافت نشد' in response_or_error else 500)
                
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
