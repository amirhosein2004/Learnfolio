from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blog.api.v1.views.blog_views import BlogViewSet


app_name = 'blog_v1'

router = DefaultRouter()
router.register(r'blogs', BlogViewSet, basename='blog')

urlpatterns = [
    path("", include(router.urls)),
]
