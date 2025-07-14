# وظایف پس‌زمینه (Background Tasks)

## Celery
برای اجرای وظایف پس‌زمینه مانند ارسال پیامک و ایمیل از Celery استفاده می‌شود.

### وظایف اصلی:
- ارسال پیامک (send_sms_task)
- ارسال ایمیل (send_email_task)
- حذف OTPهای منقضی‌شده (delete_expired_otps)

## Message Broker
RabbitMQ به عنوان message broker برای Celery استفاده می‌شود.

## زمان‌بندی وظایف
برای وظایف زمان‌بندی‌شده (مانند حذف OTPهای منقضی‌شده) از celery beat و django_celery_beat استفاده می‌شود.
