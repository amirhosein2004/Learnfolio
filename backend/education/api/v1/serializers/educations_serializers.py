from rest_framework import serializers
from education.models import Package, Video
from rest_framework.validators import UniqueValidator



class VideoSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title']  


class PackageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = [
            'id', 'title', 'slug', 'author', 'thumbnail', 'is_free',
            'price', 'status', 'total_duration', 'created_at'
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data.get('author') is None:
            data['author'] = ""
        if data.get('price') is None:
            data['price'] = ""  
        if data.get('total_duration') is None:
            data['total_duration'] = ""  
        return data


class PackageSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    view_count = serializers.IntegerField(read_only=True)
    popularity_score = serializers.FloatField(read_only=True)
    download_count = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    videos_count = serializers.SerializerMethodField(read_only=True)
    videos = VideoSimpleSerializer(read_only=True, many=True)
    
    title = serializers.CharField(
        max_length=200,
        validators=[UniqueValidator(queryset=Package.objects.all(), message="پکیجی با این عنوان قبلاً ثبت شده است")],
        error_messages={
            'required': 'عنوان پکیج نمی‌تواند خالی باشد',
            'blank': 'عنوان پکیج نمی‌تواند خالی باشد',
            'max_length': 'عنوان پکیج نمی‌تواند بیشتر از ۲۰۰ کاراکتر باشد',
        }
    )

    class Meta:
        model = Package
        fields = '__all__'
        extra_kwargs = {
            'description': {
                'required': True,
                'allow_blank': False,
                'error_messages': {
                    'required': 'توضیحات پکیج نمی‌تواند خالی باشد',
                    'blank': 'توضیحات پکیج نمی‌تواند خالی باشد',
                },
            },
            'thumbnail': {
                'required': True,
                'allow_null': False,
                'error_messages': {
                    'required': 'تصویر پکیج نمی تواند خالی باشد',
                    'null': 'تصویر پکیج نمی تواند خالی باشد',
                    'invalid': 'داده ارسالی فایل نیست. لطفاً نوع داده را بررسی کنید',
                },
            },
            'status': {
                'required': True,
                'error_messages': {
                    'required': 'وضعیت پکیج نمی تواند خالی باشد',
                    'invalid_choice': 'وضعیت انتخاب شده معتبر نیست',
                },
            },
            'price': {
                'max_digits': 10,
                'decimal_places': 2,
                'error_messages': {
                    'invalid': 'قیمت وارد شده معتبر نیست',
                    'max_digits': 'قیمت نمی تواند بیشتر از ۱۰ رقم باشد',
                    'max_decimal_places': 'قیمت نمی تواند بیشتر از ۲ رقم اعشاری باشد',
                },
            },
        }

    def get_videos_count(self, obj):
        return obj.videos.count()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data.get('author') is None:
            data['author'] = ""
        if data.get('price') is None:
            data['price'] = ""  
        if data.get('total_duration') is None:
            data['total_duration'] = ""  
        return data

    def validate_thumbnail(self, value):
        """validate thumbnail image"""
        if value.size > 5 * 1024 * 1024:  # 5MB
            raise serializers.ValidationError("حجم تصویر باید کمتر از ۵ مگابایت باشد")
        return value

    def validate_price(self, value):
        """validate price"""
        if value is not None and value < 0:
            raise serializers.ValidationError("قیمت نمی تواند منفی باشد")
        return value

    def validate(self, attrs):
        """validate general"""
        is_free = attrs.get('is_free', False)
        price = attrs.get('price')
        
        if not is_free and (price is None or price <= 0):
            raise serializers.ValidationError({
                'price': 'برای پکیج‌های غیررایگان، قیمت باید مشخص شود'
            })
        
        if is_free and price and price > 0:
            raise serializers.ValidationError({
                'price': 'پکیج‌های رایگان نمی‌توانند قیمت داشته باشند'
            })
        
        return attrs 


class VideoListSerializer(serializers.ModelSerializer):
    package_title = serializers.CharField(source='package.title', read_only=True)
    
    class Meta:
        model = Video
        fields = [
                'id', 'title', 'slug', 'package', 'order',
                'package_title', 'is_free', 'created_at'
            ]


class VideoSerializer(serializers.ModelSerializer):
    package = serializers.PrimaryKeyRelatedField(queryset=Package.objects.all())
    package_title = serializers.CharField(source='package.title', read_only=True)
    slug = serializers.SlugField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    order = serializers.IntegerField(read_only=True)

    class Meta:
        model = Video
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Video.objects.all(),
                fields=['package', 'title'],  
                message="این عنوان ویدیو در این پکیج قبلاً استفاده شده است"
            ),
        ]
        extra_kwargs = {
            'title': {
                'required': True,
                'allow_blank': False,
                'max_length': 200,
                'error_messages': {
                    'required': 'عنوان ویدیو نمی‌تواند خالی باشد',
                    'blank': 'عنوان ویدیو نمی‌تواند خالی باشد',
                    'max_length': 'عنوان ویدیو نمی‌تواند بیشتر از ۲۰۰ کاراکتر باشد',
                },
            },
            'video_file': {
                'required': True,
                'allow_null': False,
                'error_messages': {
                    'required': 'فایل ویدیو نمی‌تواند خالی باشد',
                    'null': 'فایل ویدیو نمی‌تواند خالی باشد',
                    'invalid': 'داده ارسالی فایل نیست. لطفاً نوع داده را بررسی کنید',
                },
            },
        }

    def validate_video_file(self, value):
        """validate file video"""
        if value.size > 500 * 1024 * 1024:
            raise serializers.ValidationError(
                "حجم فایل ویدیو باید کمتر از ۵۰۰ مگابایت باشد"
            )
        
        allowed_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']
        file_extension = value.name.lower().split('.')[-1] if '.' in value.name else ''
        if f'.{file_extension}' not in allowed_extensions:
            raise serializers.ValidationError(
                "mp4, avi, mkv, mov, wmv, flv, webm :فرمت فایل ویدیو پشتیبانی نمی‌شود. فرمت‌های مجاز"
            )
        
        return value
