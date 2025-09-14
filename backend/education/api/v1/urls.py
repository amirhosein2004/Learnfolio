from rest_framework.routers import DefaultRouter
from django.urls import path, include
from education.api.v1.views.educations_view import PackageViewSet, VideoViewSet


router = DefaultRouter()
router.register(r'packages', PackageViewSet, basename='package')


urlpatterns = [
    path('', include(router.urls)),

    path('packages/<package_slug>/videos/',
        VideoViewSet.as_view({
            'get': 'list',
            'post': 'create', 
        }),
        name='package-videos'
    ),

    path('packages/<package_slug>/videos/reorder/',
        VideoViewSet.as_view({
            'post': 'reorder'
        }),
        name='package-videos-reorder'
    ),

    path('packages/<package_slug>/videos/<slug>/',
        VideoViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }),
        name='package-video-detail'
    ),

    path('packages/<package_slug>/videos/<slug>/download/',
        VideoViewSet.as_view({
            'get': 'download'
        }),
        name='package-video-download'
    ),
]
