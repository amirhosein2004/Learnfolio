import logging
from rest_framework import viewsets, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from blog.models import Blog
from blog.api.v1.serializers.blog_serializers import BlogSerializer
from core.permissions import UserAdminOrReadOnly
from core.pagination import BlogPagination
from rest_framework.exceptions import ValidationError, NotFound
from django.http import Http404
from blog.schema_docs.v1.blog_schema import (
    blog_list_schema,
    blog_detail_schema,
    blog_create_schema,
    blog_update_schema,
    blog_delete_schema
)
from drf_spectacular.utils import extend_schema_view, extend_schema


logger = logging.getLogger(__name__)


@extend_schema_view(
    list=extend_schema(**blog_list_schema),
    retrieve=extend_schema(**blog_detail_schema),
    create=extend_schema(**blog_create_schema),
    update=extend_schema(**blog_update_schema),
    partial_update=extend_schema(**blog_update_schema),
    destroy=extend_schema(**blog_delete_schema),
)
class BlogViewSet(viewsets.ModelViewSet):
    """
    API endpoint for blog management.
    """
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [UserAdminOrReadOnly]
    pagination_class = BlogPagination
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title']
    
    def perform_create(self, serializer):
        """
        Save the blog with the admin profile of the current user.
        """
        serializer.save(author=self.request.user.admin_profile)

    def create(self, request, *args, **kwargs):
        """
        Create a new blog.
        """
        try:
            response = super().create(request, *args, **kwargs)
            return Response({'message': 'مقاله با موفقیت ایجاد شد', 'data': response.data}, status=201)
        except ValidationError as e:
            return Response(e.detail, status=400)
        except Exception:
            logger.error("Error creating blog", exc_info=True)
            return Response({'detail': ".خطای ناشناخته‌ای رخ داده است لطفا دوباره تلاش کنید"}, status=500)

    def update(self, request, *args, **kwargs):
        """
        Update an existing blog.
        """
        try:
            response = super().update(request, *args, **kwargs)
            return Response({'message': 'مقاله با موفقیت ویرایش شد', 'data': response.data}, status=200)
        except ValidationError as e:
            return Response(e.detail, status=400)
        except (NotFound, Http404):
            return Response({'detail': 'صفحه مورد نظر یافت نشد.'}, status=404)
        except Exception:
            logger.error("Error updating blog", exc_info=True)
            return Response({'detail': ".خطای ناشناخته‌ای رخ داده است لطفا دوباره تلاش کنید"}, status=500)

    def destroy(self, request, *args, **kwargs):
        """
        Delete an existing blog.
        """
        try:
            super().destroy(request, *args, **kwargs)
            return Response({'message': 'مقاله با موفقیت حذف شد'}, status=204)
        except ValidationError as e:
            return Response(e.detail, status=400)
        except (NotFound, Http404):
            return Response({'detail': 'صفحه مورد نظر یافت نشد.'}, status=404)
        except Exception:
            logger.error("Error deleting blog", exc_info=True)
            return Response({'detail': ".خطای ناشناخته‌ای رخ داده است لطفا دوباره تلاش کنید"}, status=500)
