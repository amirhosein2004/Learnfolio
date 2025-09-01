from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from blog.api.v1.serializers.blog_serializers import BlogSerializer
from accounts.schema_docs.v1.common_schemas import STANDARD_ERROR_RESPONSES

# GET /api/blog/v1/blogs/ - List all blogs
blog_list_schema = {
    "summary": "دریافت لیست مقالات",
    "tags": ["blog"],
    "auth": [],
}

# GET /api/blog/v1/blogs/{slug}/ - Get single blog by slug
blog_detail_schema = {
    "summary": "دریافت جزئیات مقاله",
    "tags": ["blog"],
    "auth": [],
}

# POST /api/blog/v1/blogs/ - Create new blog
blog_create_schema = {
    "summary": "ایجاد مقاله جدید",
    "tags": ["blog"],
}

# PUT/PATCH /api/blog/v1/blogs/{slug}/ - Update existing blog
blog_update_schema = {
    "summary": "ویرایش مقاله موجود",
    "tags": ["blog"],
}

# DELETE /api/blog/v1/blogs/{slug}/ - Delete existing blog
blog_delete_schema = {
    "summary": "حذف مقاله موجود",
    "tags": ["blog"],
}
