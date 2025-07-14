# ساختار دیتابیس

## User
- full_name: نام کامل
- email: ایمیل (یکتا، اختیاری)
- phone_number: شماره موبایل (یکتا، اختیاری)
- is_active: فعال بودن حساب
- is_staff: دسترسی ادمین
- date_joined: تاریخ عضویت
- last_login: آخرین ورود

## AdminProfile
- user: ارتباط یک‌به‌یک با User
- social_networks: شبکه‌های اجتماعی (JSON)
- description: توضیحات

## OTP
- email: ایمیل (اختیاری)
- phone_number: شماره موبایل (اختیاری)
- code: کد OTP
- purpose: هدف (login, register, reset)
- created_at: زمان ایجاد

### نکته
- OTPها پس از ۲ دقیقه منقضی و حذف می‌شوند.
- ایندکس ترکیبی روی (email, phone_number, code) برای جستجوی سریع‌تر.
