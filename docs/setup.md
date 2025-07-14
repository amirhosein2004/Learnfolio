# راه‌اندازی پروژه Learnfolio

## پیش‌نیازها
- Python 3.10+
- Node.js (برای فرانت‌اند)
- Docker و docker-compose (پیشنهادی برای توسعه و استقرار)

## مراحل راه‌اندازی Backend
1. نصب وابستگی‌ها:
   ```
   pip install -r requirements/base.txt
   ```
2. تنظیم متغیرهای محیطی در فایل .env
3. اجرای مهاجرت‌ها:
   ```
   python manage.py migrate
   ```
4. اجرای سرور توسعه:
   ```
   python manage.py runserver
   ```
5. اجرای Celery (در ترمینال جداگانه):
   ```
   celery -A backend worker --loglevel=info
   celery -A backend beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
   ```

## راه‌اندازی Frontend
1. نصب وابستگی‌ها:
   ```
   cd frontend
   npm install
   ```
2. اجرای سرور توسعه:
   ```
   npm run dev
   ```

## اجرای پروژه با Docker
```
docker-compose up --build
```
