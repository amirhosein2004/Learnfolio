from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from education.api.v1.serializers.educations_serializers import PackageSerializer, PackageListSerializer

package_list_schema = {
    "responses": {
        200: OpenApiResponse(
            description="لیست پکیج‌های آموزشی",
            response=PackageListSerializer(many=True),
            examples=[
                OpenApiExample(
                    name="لیست پکیج‌ها",
                    value={
                        "count": 10,
                        "next": "http://example.com/api/education/v1/packages/?page=2",
                        "previous": None,
                        "results": [
                            {
                                "id": 1,
                                "title": "آموزش Django",
                                "slug": "django-tutorial",
                                "author": "احمد محمدی",
                                "thumbnail": "/media/packages/thumbnails/django.jpg",
                                "is_free": False,
                                "price": "250000.00",
                                "status": "completed",
                                "total_duration": 7200,
                                "created_at": "2024-01-15T10:30:00Z"
                            }
                        ]
                    },
                    response_only=True,
                )
            ]
        ),
        400: OpenApiResponse(
            description="خطاهای اعتبارسنجی",
            response={"detail": "پارامترهای ارسالی نامعتبر است"}
        )
    },
    "summary": "دریافت لیست پکیج‌های آموزشی",
    "description": (
        "دریافت لیست پکیج‌های آموزشی با قابلیت فیلتر و جستجو\n\n"
        "- فیلتر بر اساس رایگان بودن: `is_free=true/false`\n"
        "- جستجو در عنوان: `search=عنوان`\n"
        "- مرتب‌سازی: `ordering=-created_at,view_count,popularity_score`\n"
        "- صفحه‌بندی پشتیبانی می‌شود"
    ),
    "tags": ["packages"]
}

package_create_schema = {
    "request": PackageSerializer,
    "responses": {
        201: OpenApiResponse(
            description="پکیج با موفقیت ایجاد شد",
            response=PackageSerializer,
            examples=[
                OpenApiExample(
                    name="پکیج جدید",
                    value={
                        "id": 1,
                        "title": "آموزش React",
                        "slug": "react-tutorial",
                        "description": "آموزش کامل React از صفر تا صد",
                        "status": "recording",
                        "thumbnail": "/media/packages/thumbnails/react.jpg",
                        "is_free": False,
                        "price": "300000.00",
                        "author": "علی احمدی",
                        "created_at": "2024-01-15T10:30:00Z"
                    },
                    response_only=True,
                )
            ]
        ),
        400: OpenApiResponse(
            description="خطاهای اعتبارسنجی",
            response={
                "title": ["عنوان پکیج نمی‌تواند خالی باشد"],
                "description": ["توضیحات پکیج نمی‌تواند خالی باشد"],
                "thumbnail": ["تصویر پکیج نمی تواند خالی باشد"]
            }
        ),
        401: OpenApiResponse(
            description="عدم احراز هویت",
            response={"detail": "Authentication credentials were not provided."}
        ),
        403: OpenApiResponse(
            description="عدم دسترسی",
            response={"detail": "شما اجازه انجام این عمل را ندارید"}
        )
    },
    "summary": "ایجاد پکیج آموزشی جدید",
    "description": (
        "ایجاد پکیج آموزشی جدید توسط ادمین\n\n"
        "- نیاز به احراز هویت و دسترسی ادمین\n"
        "- عنوان باید منحصر به فرد باشد\n"
        "- تصویر و توضیحات الزامی است\n"
        "- اسلاگ به صورت خودکار تولید می‌شود"
    ),
    "tags": ["packages"]
}

package_retrieve_schema = {
    "responses": {
        200: OpenApiResponse(
            description="جزئیات پکیج آموزشی",
            response=PackageSerializer,
            examples=[
                OpenApiExample(
                    name="جزئیات پکیج",
                    value={
                        "id": 1,
                        "title": "آموزش Django",
                        "slug": "django-tutorial",
                        "description": "آموزش کامل Django از صفر تا صد",
                        "status": "completed",
                        "thumbnail": "/media/packages/thumbnails/django.jpg",
                        "is_free": False,
                        "price": "250000.00",
                        "total_duration": 7200,
                        "view_count": 150,
                        "popularity_score": 8.5,
                        "download_count": 45,
                        "author": "احمد محمدی",
                        "videos_count": 12,
                        "videos": [
                            {"id": 1, "title": "مقدمه"},
                            {"id": 2, "title": "نصب Django"}
                        ],
                        "created_at": "2024-01-15T10:30:00Z"
                    },
                    response_only=True,
                )
            ]
        ),
        404: OpenApiResponse(
            description="پکیج یافت نشد",
            response={"detail": "پکیج مورد نظر یافت نشد"}
        )
    },
    "summary": "دریافت جزئیات پکیج آموزشی",
    "description": (
        "دریافت جزئیات کامل پکیج آموزشی\n\n"
        "- تعداد بازدید به صورت خودکار افزایش می‌یابد\n"
        "- شامل لیست ویدیوهای پکیج\n"
        "- اطلاعات نویسنده و آمار پکیج"
    ),
    "tags": ["packages"]
}

package_update_schema = {
    "request": PackageSerializer,
    "responses": {
        200: OpenApiResponse(
            description="پکیج با موفقیت بروزرسانی شد",
            response=PackageSerializer
        ),
        400: OpenApiResponse(
            description="خطاهای اعتبارسنجی",
            response={
                "title": ["پکیجی با این عنوان قبلاً ثبت شده است"],
                "price": ["برای پکیج‌های غیررایگان، قیمت باید مشخص شود"]
            }
        ),
        401: OpenApiResponse(
            description="عدم احراز هویت",
            response={"detail": "Authentication credentials were not provided."}
        ),
        403: OpenApiResponse(
            description="عدم دسترسی",
            response={"detail": "شما اجازه انجام این عمل را ندارید"}
        ),
        404: OpenApiResponse(
            description="پکیج یافت نشد",
            response={"detail": "پکیج مورد نظر یافت نشد"}
        )
    },
    "summary": "بروزرسانی پکیج آموزشی",
    "description": (
        "بروزرسانی اطلاعات پکیج آموزشی\n\n"
        "- نیاز به احراز هویت و دسترسی ادمین\n"
        "- اعتبارسنجی قیمت برای پکیج‌های غیررایگان\n"
        "- نویسنده پکیج تغییر نمی‌کند"
    ),
    "tags": ["packages"]
}

package_delete_schema = {
    "responses": {
        204: OpenApiResponse(
            description="پکیج با موفقیت حذف شد",
            response={"message": "پکیج با موفقیت حذف شد"}
        ),
        401: OpenApiResponse(
            description="عدم احراز هویت",
            response={"detail": "Authentication credentials were not provided."}
        ),
        403: OpenApiResponse(
            description="عدم دسترسی",
            response={"detail": "شما اجازه انجام این عمل را ندارید"}
        ),
        404: OpenApiResponse(
            description="پکیج یافت نشد",
            response={"detail": "پکیج مورد نظر یافت نشد"}
        ),
        500: OpenApiResponse(
            description="خطای سرور",
            response={"detail": "خطای ناشناخته ای رخ داده است لطفا دوباره تلاش کنید"}
        )
    },
    "summary": "حذف پکیج آموزشی",
    "description": (
        "حذف پکیج آموزشی\n\n"
        "- نیاز به احراز هویت و دسترسی ادمین\n"
        "- حذف پکیج باعث حذف تمام ویدیوهای آن می‌شود"
    ),
    "tags": ["packages"]
}
