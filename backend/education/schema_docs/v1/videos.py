from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from education.api.v1.serializers.educations_serializers import VideoSerializer, VideoListSerializer

video_list_schema = {
    "responses": {
        200: OpenApiResponse(
            description="لیست ویدیوهای پکیج",
            response=VideoListSerializer(many=True),
            examples=[
                OpenApiExample(
                    name="لیست ویدیوها",
                    value={
                        "count": 5,
                        "next": None,
                        "previous": None,
                        "results": [
                            {
                                "id": 1,
                                "title": "مقدمه",
                                "slug": "introduction",
                                "package": 1,
                                "order": 0,
                                "package_title": "آموزش Django",
                                "is_free": True,
                                "created_at": "2024-01-15T10:30:00Z"
                            }
                        ]
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
    "summary": "دریافت لیست ویدیوهای پکیج",
    "description": (
        "دریافت لیست ویدیوهای یک پکیج آموزشی\n\n"
        "- ویدیوها بر اساس ترتیب مرتب می‌شوند\n"
        "- شامل اطلاعات پایه ویدیو و پکیج\n"
        "- صفحه‌بندی پشتیبانی می‌شود"
    ),
    "tags": ["videos"]
}

video_create_schema = {
    "request": VideoSerializer,
    "responses": {
        201: OpenApiResponse(
            description="ویدیو با موفقیت ایجاد شد",
            response=VideoSerializer,
            examples=[
                OpenApiExample(
                    name="ویدیو جدید",
                    value={
                        "id": 1,
                        "title": "مقدمه",
                        "slug": "introduction",
                        "description": "مقدمه‌ای بر آموزش",
                        "package": 1,
                        "package_title": "آموزش Django",
                        "video_file": "/media/videos/django-tutorial/intro.mp4",
                        "is_free": True,
                        "order": 0,
                        "created_at": "2024-01-15T10:30:00Z"
                    },
                    response_only=True,
                )
            ]
        ),
        400: OpenApiResponse(
            description="خطاهای اعتبارسنجی",
            response={
                "title": ["عنوان ویدیو نمی‌تواند خالی باشد"],
                "video_file": ["فایل ویدیو نمی‌تواند خالی باشد"],
                "non_field_errors": ["این عنوان ویدیو در این پکیج قبلاً استفاده شده است"]
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
    "summary": "ایجاد ویدیو جدید در پکیج",
    "description": (
        "ایجاد ویدیو جدید در پکیج آموزشی\n\n"
        "- نیاز به احراز هویت و دسترسی مناسب\n"
        "- عنوان ویدیو در هر پکیج باید منحصر به فرد باشد\n"
        "- فایل ویدیو الزامی است (حداکثر 500MB)\n"
        "- فرمت‌های پشتیبانی: mp4, avi, mkv, mov, wmv, flv, webm\n"
        "- ترتیب به صورت خودکار تعیین می‌شود"
    ),
    "tags": ["videos"]
}

video_retrieve_schema = {
    "responses": {
        200: OpenApiResponse(
            description="جزئیات ویدیو",
            response=VideoSerializer,
            examples=[
                OpenApiExample(
                    name="جزئیات ویدیو",
                    value={
                        "id": 1,
                        "title": "مقدمه",
                        "slug": "introduction",
                        "description": "مقدمه‌ای بر آموزش Django",
                        "package": 1,
                        "package_title": "آموزش Django",
                        "video_file": "/media/videos/django-tutorial/intro.mp4",
                        "is_free": True,
                        "order": 0,
                        "created_at": "2024-01-15T10:30:00Z",
                        "updated_at": "2024-01-15T10:30:00Z"
                    },
                    response_only=True,
                )
            ]
        ),
        404: OpenApiResponse(
            description="ویدیو یافت نشد",
            response={"detail": "ویدیو مورد نظر یافت نشد"}
        )
    },
    "summary": "دریافت جزئیات ویدیو",
    "description": (
        "دریافت جزئیات کامل ویدیو\n\n"
        "- شامل اطلاعات کامل ویدیو و پکیج\n"
        "- لینک فایل ویدیو برای دانلود"
    ),
    "tags": ["videos"]
}

video_update_schema = {
    "request": VideoSerializer,
    "responses": {
        200: OpenApiResponse(
            description="ویدیو با موفقیت بروزرسانی شد",
            response=VideoSerializer
        ),
        400: OpenApiResponse(
            description="خطاهای اعتبارسنجی",
            response={
                "title": ["این عنوان ویدیو در این پکیج قبلاً استفاده شده است"],
                "video_file": ["حجم فایل ویدیو باید کمتر از ۵۰۰ مگابایت باشد"]
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
            description="ویدیو یافت نشد",
            response={"detail": "ویدیو مورد نظر یافت نشد"}
        )
    },
    "summary": "بروزرسانی ویدیو",
    "description": (
        "بروزرسانی اطلاعات ویدیو\n\n"
        "- نیاز به احراز هویت و دسترسی مناسب\n"
        "- اعتبارسنجی فایل ویدیو و عنوان\n"
        "- ترتیب ویدیو تغییر نمی‌کند"
    ),
    "tags": ["videos"]
}

video_delete_schema = {
    "responses": {
        204: OpenApiResponse(
            description="ویدیو با موفقیت حذف شد"
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
            description="ویدیو یافت نشد",
            response={"detail": "ویدیو مورد نظر یافت نشد"}
        )
    },
    "summary": "حذف ویدیو",
    "description": (
        "حذف ویدیو از پکیج\n\n"
        "- نیاز به احراز هویت و دسترسی مناسب\n"
        "- فایل ویدیو نیز حذف می‌شود"
    ),
    "tags": ["videos"]
}

video_reorder_schema = {
    "request": {
        "type": "object",
        "properties": {
            "order": {
                "type": "array",
                "items": {"type": "integer"},
                "description": "آرایه‌ای از ID ویدیوها به ترتیب جدید"
            }
        },
        "required": ["order"]
    },
    "responses": {
        200: OpenApiResponse(
            description="ترتیب ویدیوها با موفقیت تغییر کرد",
            response={"message": "ترتیب ویدیوها با موفقیت تغییر کرد"},
            examples=[
                OpenApiExample(
                    name="تغییر ترتیب موفق",
                    value={"message": "ترتیب ویدیوها با موفقیت تغییر کرد"},
                    response_only=True,
                )
            ]
        ),
        400: OpenApiResponse(
            description="خطا در داده‌های ارسالی",
            response={"detail": "آرایه ترتیب نامعتبر است"}
        ),
        401: OpenApiResponse(
            description="عدم احراز هویت",
            response={"detail": "Authentication credentials were not provided."}
        ),
        403: OpenApiResponse(
            description="عدم دسترسی",
            response={"detail": "شما اجازه انجام این عمل را ندارید"}
        ),
        500: OpenApiResponse(
            description="خطای سرور",
            response={"detail": "خطا در تغییر ترتیب ویدیوها"}
        )
    },
    "summary": "تغییر ترتیب ویدیوهای پکیج",
    "description": (
        "تغییر ترتیب ویدیوهای یک پکیج\n\n"
        "- نیاز به احراز هویت و دسترسی مناسب\n"
        "- آرایه order شامل ID ویدیوها به ترتیب جدید\n"
        "- ویدیوهای موجود در آرایه بروزرسانی می‌شوند"
    ),
    "tags": ["videos"]
}

video_download_schema = {
    "responses": {
        200: OpenApiResponse(
            description="دانلود فایل ویدیو",
            response="application/octet-stream",
            examples=[
                OpenApiExample(
                    name="دانلود موفق",
                    description="فایل ویدیو برای دانلود ارسال می‌شود",
                    response_only=True,
                )
            ]
        ),
        404: OpenApiResponse(
            description="فایل ویدیو یافت نشد",
            response={"detail": "فایل ویدیو یافت نشد"}
        ),
        401: OpenApiResponse(
            description="عدم احراز هویت",
            response={"detail": "Authentication credentials were not provided."}
        ),
        403: OpenApiResponse(
            description="عدم دسترسی",
            response={"detail": "شما اجازه دسترسی به این ویدیو را ندارید"}
        ),
        500: OpenApiResponse(
            description="خطای سرور",
            response={"detail": "خطا در دانلود فایل"}
        )
    },
    "summary": "دانلود فایل ویدیو",
    "description": (
        "دانلود فایل ویدیو\n\n"
        "- نیاز به احراز هویت و دسترسی مناسب\n"
        "- تعداد دانلود پکیج افزایش می‌یابد\n"
        "- پشتیبانی از ذخیره‌سازی محلی و ابری"
    ),
    "tags": ["videos"]
}
