from rest_framework import serializers
from blog.models import Blog
from rest_framework.validators import UniqueValidator


class BlogListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'image', 'author', 'created_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['author'] is None:
            data['author'] = ""
        return data


class BlogDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    title = serializers.CharField(
        max_length=200,
        validators=[UniqueValidator(queryset=Blog.objects.all(), message="مقاله‌ای با این عنوان قبلاً ثبت شده است")]
    )

    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'content', 'image', 'author', 'created_at', 'updated_at']
        extra_kwargs = {
            'title': {
                'required': True,
                'allow_blank': False,
                'max_length': 200,
                'error_messages': {
                    'required': 'عنوان مقاله نمی تواند خالی باشد',
                    'blank': 'عنوان مقاله نمی تواند خالی باشد',
                    'max_length': 'عنوان مقاله نمی تواند بیشتر از ۲۰۰ کاراکتر باشد',
                },
            },
            'content': {
                'required': True,
                'allow_blank': False,
                'error_messages': {
                    'required': 'محتوای مقاله نمی تواند خالی باشد',
                    'blank': 'محتوای مقاله نمی تواند خالی باشد',
                },
            },
            'image': {
                'required': True,
                'allow_null': False,
                'error_messages': {
                    'required': 'تصویر مقاله نمی تواند خالی باشد',
                    'null': 'تصویر مقاله نمی تواند خالی باشد',
                    'invalid': 'داده ارسالی فایل نیست. لطفا نوع داده را بررسی کنید',
                },
            },
        }


    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['author'] is None:
            data['author'] = ""
        return data

    # NOTE: later we can add advance image validation for scan image file
    def validate_image(self, value):
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("حجم تصویر باید کمتر از ۵ مگابایت باشد")
        return value
