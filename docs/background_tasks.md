# وظایف پس‌زمینه (Background Tasks)

برای انجام کارهای زمان‌بر و غیرهمزمان مانند ارسال پیامک، ایمیل و پاکسازی داده‌های منقضی‌شده از Celery استفاده می‌شود.

## تسک‌ها (Tasks)

### ارسال پیامک (send\_sms\_task)

وظیفه ارسال پیامک‌های ارسالی به کاربران به صورت غیرهمزمان را بر عهده دارد.

### ارسال ایمیل (send\_email\_task)

برای ارسال ایمیل‌های مختلف (اعلانات، تاییدها و ...) در پس‌زمینه اجرا می‌شود تا عملکرد سیستم سریع‌تر باشد.

### پاکسازی توکن‌های منقضی‌شده (cleanup\_expired\_tokens)

این تسک با حذف تمامی توکن‌های منقضی‌شده که در دیتابیس باقی مانده‌اند، به بهبود امنیت و کارایی سیستم کمک می‌کند. این کار باعث کاهش حجم داده‌های اضافی و جلوگیری از استفاده احتمالی توکن‌های منقضی‌شده می‌شود.

مثال کد تسک:

```python
import logging
from celery import shared_task
from django.utils.timezone import now
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

logger = logging.getLogger(__name__)

@shared_task
def cleanup_expired_tokens():
    deleted_count, _ = OutstandingToken.objects.filter(expires_at__lt=now()).delete()
    logger.info(f"Cleaned up {deleted_count} expired tokens and associated blacklisted entries.")
```

## Message Broker

برای مدیریت صف‌ها و ارسال پیام‌ها بین کلاینت و Celery، از RabbitMQ به عنوان message broker استفاده می‌شود.

## زمان‌بندی وظایف (Scheduling)

وظایف زمان‌بندی‌شده مانند پاکسازی دوره‌ای توکن‌های منقضی‌شده، با استفاده از `celery beat` و کتابخانه `django_celery_beat` انجام می‌شود. این ابزارها به صورت خودکار و منظم تسک‌ها را در زمان‌های مشخص اجرا می‌کنند.

---