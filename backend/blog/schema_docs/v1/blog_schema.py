from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from blog.api.v1.serializers.blog_serializers import BlogListSerializer, BlogDetailSerializer
from accounts.schema_docs.v1.common_schemas import STANDARD_ERROR_RESPONSES

# GET /api/blog/v1/blogs/ - List all blogs
blog_list_schema = {
    "request": BlogListSerializer,
    "summary": "دریافت لیست مقالات",
    "tags": ["blog"],
    "auth": [],
}

# GET /api/blog/v1/blogs/{slug}/ - Get single blog by slug
blog_detail_schema = {
    "request": BlogDetailSerializer,
    "summary": "دریافت جزئیات مقاله",
    "tags": ["blog"],
    "auth": [],
}

# POST /api/blog/v1/blogs/ - Create new blog
blog_create_schema = {
    "request": BlogDetailSerializer,
    "summary": "ایجاد مقاله جدید",
    "tags": ["blog"],
    "responses": {
        201: OpenApiResponse(
            description="مقاله با موفقیت ایجاد شد",
            examples=[
                OpenApiExample(
                    "Success",
                    value={"message": "مقاله با موفقیت ایجاد شد", "data": {}},
                    response_only=True,
                )
            ]
        ),
        400: OpenApiResponse(description="خطای اعتبارسنجی"),
        500: OpenApiResponse(
            description="خطای سرور",
            examples=[
                OpenApiExample(
                    "Server Error",
                    value={"detail": "خطای ناشناخته‌ای رخ داده است لطفا دوباره تلاش کنید."},
                    response_only=True,
                )
            ]
        ),
    },
}

# PUT/PATCH /api/blog/v1/blogs/{slug}/ - Update existing blog
blog_update_schema = {
    "request": BlogDetailSerializer,
    "summary": "ویرایش مقاله موجود",
    "tags": ["blog"],
    "responses": {
        200: OpenApiResponse(
            description="مقاله با موفقیت ویرایش شد",
            examples=[
                OpenApiExample(
                    "Success",
                    value={"message": "مقاله با موفقیت ویرایش شد", "data": {}},
                    response_only=True,
                )
            ]
        ),
        400: OpenApiResponse(description="خطای اعتبارسنجی"),
        404: OpenApiResponse(
            description="مقاله یافت نشد",
            examples=[
                OpenApiExample(
                    "Not Found",
                    value={"detail": "صفحه مورد نظر یافت نشد."},
                    response_only=True,
                )
            ]
        ),
        500: OpenApiResponse(
            description="خطای سرور",
            examples=[
                OpenApiExample(
                    "Server Error",
                    value={"detail": "خطای ناشناخته‌ای رخ داده است لطفا دوباره تلاش کنید."},
                    response_only=True,
                )
            ]
        ),
    },
}

# DELETE /api/blog/v1/blogs/{slug}/ - Delete existing blog
blog_delete_schema = {
    "summary": "حذف مقاله موجود",
    "tags": ["blog"],
    "responses": {
        204: OpenApiResponse(
            description="مقاله با موفقیت حذف شد",
            examples=[
                OpenApiExample(
                    "Success",
                    value={"message": "مقاله با موفقیت حذف شد"},
                    response_only=True,
                )
            ]
        ),
        400: OpenApiResponse(description="خطای اعتبارسنجی"),
        404: OpenApiResponse(
            description="مقاله یافت نشد",
            examples=[
                OpenApiExample(
                    "Not Found",
                    value={"detail": "صفحه مورد نظر یافت نشد."},
                    response_only=True,
                )
            ]
        ),
        500: OpenApiResponse(
            description="خطای سرور",
            examples=[
                OpenApiExample(
                    "Server Error",
                    value={"detail": "خطای ناشناخته‌ای رخ داده است لطفا دوباره تلاش کنید."},
                    response_only=True,
                )
            ]
        ),
    },
}
