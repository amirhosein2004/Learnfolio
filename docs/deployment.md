## 🔧 دایرکتوری‌های توسعه که در زمان دیپلوی نباید مستقر شوند

در زمان استقرار پروژه در محیط Production، برخی دایرکتوری‌ها فقط مخصوص توسعه و مستندسازی هستند و نباید در محیط اجرایی (Docker Image یا سرور) مستقر شوند.

### 📁 `schema_docs/`
این دایرکتوری شامل داکیومنت‌های `drf-spectacular` و توضیحات Swagger است که فقط در زمان توسعه (`DEBUG=True`) مورد استفاده قرار می‌گیرند.

- این دایرکتوری از طریق تنظیمات `urls.py` در زمان `DEBUG=False` غیرفعال است.
- همچنین در فایل `.dockerignore` مشخص شده که این دایرکتوری در زمان ساخت Docker Image نهایی کپی نشود.

```dockerignore
schema_docs/

```

# استقرار پروژه Learnfolio

## پیش‌نیازها
- Docker و docker-compose
- تنظیم فایل .env با مقادیر مناسب

## اجرای پروژه
1. ساخت ایمیج‌ها و اجرای سرویس‌ها:
   ```
   docker-compose up --build
   ```
2. سرویس‌های اصلی:
   - web: اجرای Django
   - celery: اجرای workerهای Celery
   - celery_beat: زمان‌بندی وظایف
   - db: پایگاه داده PostgreSQL
   - rabbitmq: message broker

## نکات مهم
- پورت 8000 برای وب، 5432 برای دیتابیس، 5672 و 15672 برای RabbitMQ
- تنظیم متغیرهای محیطی در .env (مانند SECRET_KEY، KAVENEGAR_API_KEY و ...)
- برای محیط production، DEBUG را False قرار دهید و ALLOWED_HOSTS را تنظیم کنید.
