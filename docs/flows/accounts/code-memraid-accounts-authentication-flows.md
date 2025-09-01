# فلوهای احراز هویت - Accounts App

این سند شامل کد های نمودارهای ساده فلوهای احراز هویت سیستم Learnfolio است که با استفاده از Mermaid.js ترسیم شده است.

## 1. فلو ارسال شناسه (Identity Submission)

این فلو زمانی اجرا می‌شود که کاربر ایمیل یا شماره تلفن خود را برای ورود یا ثبت‌نام ارسال می‌کند.

```
flowchart TD
    %% ===============================
    %% کلاینت و ورودی
    %% ===============================
    A[💻 کلاینت<br>درخواست ارسال شناسه] --> B[🛠️ IdentitySubmissionAPIView]
    
    %% ===============================
    %% بررسی امنیت و محدودیت
    %% ===============================
    B --> C{🔒 بررسی CAPTCHA<br>و Rate Limiting}
    C -->|موفق ✅| D[📝 IdentitySerializer<br>اعتبارسنجی داده‌ها]
    C -->|ناموفق ❌| E[⚠️ خطا: محدودیت دسترسی]
    
    %% ===============================
    %% پردازش هویت و تشخیص نوع کاربر
    %% ===============================
    D --> F[🔑 AuthService<br>handle_identity_submission]
    F --> G[🕵️ ValidationService<br>تشخیص نوع کاربر]
    
    H{👤 کاربر موجود است؟}  
    G --> H
    H -->|بله ✅| I[purpose = login]
    H -->|خیر ❌| J[purpose = register]
    
    %% ===============================
    %% مسیر نوع شناسه
    %% ===============================
    I --> K{📧/📱 نوع شناسه}
    J --> K
    
    %% ===============================
    %% تولید کد یا لینک تایید
    %% ===============================
    K -->|📧 ورود| L[🗝️ OTPCacheService<br>تولید کد یکبار مصرف]
    K -->|📧 ثبت‌نام| M[🔗 تولید لینک تایید ایمیل]
    K -->|📱 تلفن| N[🗝️ OTPCacheService<br>تولید کد یکبار مصرف]
    
    %% ===============================
    %% ذخیره‌سازی و ارسال
    %% ===============================
    L --> O[💾 Redis Cache<br>ذخیره کد ۲ دقیقه]
    N --> O
    M --> P[🔐 تولید توکن ایمیل]
    
    O --> Q[✉️ send_email_task<br>ارسال کد]
    O --> R[📲 send_sms_task<br>ارسال کد]
    P --> S[✉️ send_email_task<br>ارسال لینک تایید]
    
    %% ===============================
    %% Cooldown و پاسخ نهایی
    %% ===============================
    Q --> T[⏱️ تنظیم Cooldown]
    R --> T
    S --> T
    
    T --> U[✅ پاسخ موفق به کلاینت]
    E --> V[❌ پاسخ خطا به کلاینت]

    %% ===============================
    %% استایل‌ها
    %% ===============================
    style A fill:#e3f2fd,stroke:#42a5f5,stroke-width:2px,stroke-dasharray: 4 2
    style B fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style C fill:#fff9c4,stroke:#fbc02d,stroke-width:2px
    style D fill:#c5cae9,stroke:#5c6bc0,stroke-width:2px
    style F fill:#d1c4e9,stroke:#7e57c2,stroke-width:2px
    style G fill:#e1bee7,stroke:#ab47bc,stroke-width:2px
    style H fill:#ffe0b2,stroke:#ffb74d,stroke-width:2px,stroke-dasharray: 2 2
    style K fill:#b2dfdb,stroke:#26a69a,stroke-width:2px
    style L fill:#c8e6c9,stroke:#43a047,stroke-width:2px
    style M fill:#dcedc8,stroke:#7cb342,stroke-width:2px
    style N fill:#c8e6c9,stroke:#43a047,stroke-width:2px
    style O fill:#e0f7fa,stroke:#00acc1,stroke-width:2px
    style P fill:#f0f4c3,stroke:#c0ca33,stroke-width:2px
    style Q fill:#ffe082,stroke:#ffa000,stroke-width:2px
    style R fill:#ffe082,stroke:#ffa000,stroke-width:2px
    style S fill:#fff59d,stroke:#fbc02d,stroke-width:2px
    style T fill:#b3e5fc,stroke:#039be5,stroke-width:2px
    style U fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style V fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style E fill:#ffcdd2,stroke:#c62828,stroke-width:2px
```

## 2. فلو تایید کد OTP

این فلو برای تایید کد OTP ارسال شده به ایمیل یا شماره تلفن استفاده می‌شود.

```
flowchart TD
    %% ===============================
    %% کلاینت و ورودی OTP
    %% ===============================
    A[💻 کلاینت<br>ارسال کد OTP] --> B[🛠️ OTPOrVerificationAPIView]
    
    %% ===============================
    %% بررسی امنیت و محدودیت
    %% ===============================
    B --> C{🔒 بررسی CAPTCHA<br>و Rate Limiting}
    C -->|موفق ✅| D[📝 AuthenticateOTPVerificationSerializer<br>اعتبارسنجی داده‌ها]
    C -->|ناموفق ❌| E[⚠️ خطا: محدودیت دسترسی]
    
    %% ===============================
    %% بررسی OTP در کش
    %% ===============================
    D --> F[🕵️ ValidationService<br>بررسی کد در کش]
    F --> G[💾 Redis Cache<br>جستجوی کد]
    
    %% ===============================
    %% اعتبارسنجی کد
    %% ===============================
    G --> H{🔑 کد معتبر است؟}
    H -->|بله ✅| I[🗑️ حذف کد از کش]
    H -->|خیر ❌| J[⚠️ خطا: کد نامعتبر یا منقضی]
    
    %% ===============================
    %% ورود یا ثبت‌نام کاربر
    %% ===============================
    I --> K[🔑 AuthService<br>login_or_register_user]
    K --> L[🕵️ ValidationService<br>تشخیص نوع عملیات]
    
    M{📌 نوع عملیات}  
    L --> M
    M -->|ثبت‌نام 🆕| N[💾 Database<br>ایجاد کاربر جدید]
    M -->|ورود 🔑| O[💾 Database<br>یافتن کاربر موجود]
    
    %% ===============================
    %% تولید توکن و پاسخ
    %% ===============================
    N --> P[🔐 JWT Service<br>تولید access_token و refresh_token]
    O --> P
    P --> Q[✅ پاسخ موفق<br>+ access_token + refresh_token]
    
    %% ===============================
    %% مسیر خطا
    %% ===============================
    E --> R[❌ پاسخ خطا: محدودیت]
    J --> S[❌ پاسخ خطا: کد نامعتبر]

    %% ===============================
    %% استایل‌ها
    %% ===============================
    style A fill:#e3f2fd,stroke:#42a5f5,stroke-width:2px,stroke-dasharray: 4 2
    style B fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style C fill:#fff9c4,stroke:#fbc02d,stroke-width:2px
    style D fill:#c5cae9,stroke:#5c6bc0,stroke-width:2px
    style F fill:#d1c4e9,stroke:#7e57c2,stroke-width:2px
    style G fill:#e1bee7,stroke:#ab47bc,stroke-width:2px
    style H fill:#ffe0b2,stroke:#ffb74d,stroke-width:2px,stroke-dasharray: 2 2
    style I fill:#b2dfdb,stroke:#26a69a,stroke-width:2px
    style K fill:#c8e6c9,stroke:#43a047,stroke-width:2px
    style L fill:#dcedc8,stroke:#7cb342,stroke-width:2px
    style M fill:#fff9c4,stroke:#fdd835,stroke-width:2px,stroke-dasharray: 2 2
    style N fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style O fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style P fill:#b3e5fc,stroke:#039be5,stroke-width:2px
    style Q fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style R fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style S fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style E fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style J fill:#ffcdd2,stroke:#c62828,stroke-width:2px
```

## 3. فلو تایید لینک ایمیل

این فلو برای تایید لینک‌های ارسال شده به ایمیل در فرآیند ثبت‌نام استفاده می‌شود.

```
flowchart TD
    %% ===============================
    %% کلاینت و کلیک روی لینک ایمیل
    %% ===============================
    A[💻 کلاینت<br>کلیک روی لینک ایمیل] --> B[🛠️ LinkVerificationAPIView]
    
    %% ===============================
    %% بررسی امنیت و محدودیت
    %% ===============================
    B --> C{🔒 بررسی CAPTCHA<br>و Rate Limiting}
    C -->|موفق ✅| D[📝 RegisterConfirmationLinkSerializer<br>اعتبارسنجی داده‌ها]
    C -->|ناموفق ❌| E[⚠️ خطا: محدودیت دسترسی]
    
    %% ===============================
    %% بررسی توکن ایمیل
    %% ===============================
    D --> F[🕵️ ValidationService<br>بررسی توکن ایمیل]
    F --> G{🔑 توکن معتبر است؟}
    
    G -->|بله ✅| H[🔑 AuthService<br>ثبت‌نام کاربر جدید]
    G -->|خیر ❌| I[⚠️ خطا: توکن نامعتبر یا منقضی]
    
    %% ===============================
    %% ایجاد کاربر و تولید توکن
    %% ===============================
    H --> J[💾 Database<br>ایجاد کاربر با ایمیل]
    J --> K[🔐 JWT Service<br>تولید access_token و refresh_token]
    K --> L[✅ پاسخ موفق<br>+ access_token + refresh_token]
    
    %% ===============================
    %% مسیر خطا
    %% ===============================
    E --> M[❌ پاسخ خطا: محدودیت]
    I --> N[❌ پاسخ خطا: توکن نامعتبر]

    %% ===============================
    %% استایل‌ها
    %% ===============================
    style A fill:#e3f2fd,stroke:#42a5f5,stroke-width:2px,stroke-dasharray: 4 2
    style B fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style C fill:#fff9c4,stroke:#fbc02d,stroke-width:2px
    style D fill:#c5cae9,stroke:#5c6bc0,stroke-width:2px
    style F fill:#d1c4e9,stroke:#7e57c2,stroke-width:2px
    style G fill:#ffe0b2,stroke:#ffb74d,stroke-width:2px,stroke-dasharray: 2 2
    style H fill:#c8e6c9,stroke:#43a047,stroke-width:2px
    style J fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style K fill:#b3e5fc,stroke:#039be5,stroke-width:2px
    style L fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style M fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style N fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style E fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style I fill:#ffcdd2,stroke:#c62828,stroke-width:2px
```

## 4. فلو ارسال مجدد کد/لینک

این فلو برای ارسال مجدد کد OTP یا لینک تایید استفاده می‌شود.

```
flowchart TD
    %% ===============================
    %% کلاینت و درخواست ارسال مجدد
    %% ===============================
    A[💻 کلاینت<br>درخواست ارسال مجدد] --> B[🛠️ ResendOTPOrLinkAPIView]
    
    %% ===============================
    %% بررسی امنیت و محدودیت
    %% ===============================
    B --> C{🔒 بررسی CAPTCHA<br>و Rate Limiting}
    C -->|موفق ✅| D[📝 IdentitySerializer<br>اعتبارسنجی داده‌ها]
    C -->|ناموفق ❌| E[⚠️ خطا: محدودیت دسترسی]
    
    %% ===============================
    %% بررسی Cooldown
    %% ===============================
    D --> F[⏱️ CacheService<br>بررسی cooldown]
    F --> G[💾 Redis Cache<br>بررسی زمان باقی‌مانده]
    
    G --> H{⏳ cooldown فعال است؟}
    H -->|بله ❌| I[⚠️ خطا: باید صبر کنید]
    H -->|خیر ✅| J[🔁 AuthService<br>ارسال مجدد]
    
    %% ===============================
    %% مسیر ارسال مجدد
    %% ===============================
    J --> K[🔄 همان فلو ارسال اولیه]
    K --> L[⏱️ تنظیم cooldown جدید]
    L --> M[✅ پاسخ موفق<br>کد/لینک ارسال شد]
    
    %% ===============================
    %% مسیر خطا
    %% ===============================
    E --> N[❌ پاسخ خطا: محدودیت]
    I --> O[❌ پاسخ خطا: زمان انتظار]

    %% ===============================
    %% استایل‌ها
    %% ===============================
    style A fill:#e3f2fd,stroke:#42a5f5,stroke-width:2px,stroke-dasharray: 4 2
    style B fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style C fill:#fff9c4,stroke:#fbc02d,stroke-width:2px
    style D fill:#c5cae9,stroke:#5c6bc0,stroke-width:2px
    style F fill:#d1c4e9,stroke:#7e57c2,stroke-width:2px
    style G fill:#e1bee7,stroke:#ab47bc,stroke-width:2px
    style H fill:#ffe0b2,stroke:#ffb74d,stroke-width:2px,stroke-dasharray: 2 2
    style J fill:#c8e6c9,stroke:#43a047,stroke-width:2px
    style K fill:#dcedc8,stroke:#7cb342,stroke-width:2px
    style L fill:#b3e5fc,stroke:#039be5,stroke-width:2px
    style M fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style N fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style O fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style E fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style I fill:#ffcdd2,stroke:#c62828,stroke-width:2px
```

## 5. فلو ورود با رمز عبور

این فلو برای ورود کاربران با استفاده از رمز عبور استفاده می‌شود.

```
flowchart TD
    %% ===============================
    %% کلاینت و ورود با رمز عبور
    %% ===============================
    A[💻 کلاینت<br>ورود با رمز عبور] --> B[🛠️ PasswordLoginAPIView]
    
    %% ===============================
    %% بررسی امنیت و محدودیت
    %% ===============================
    B --> C{🔒 بررسی CAPTCHA<br>و Rate Limiting}
    C -->|موفق ✅| D[📝 PasswordLoginSerializer<br>اعتبارسنجی داده‌ها]
    C -->|ناموفق ❌| E[⚠️ خطا: محدودیت دسترسی]
    
    %% ===============================
    %% بررسی کاربر و رمز عبور
    %% ===============================
    D --> F[🕵️ ValidationService<br>بررسی کاربر و رمز]
    F --> G[💾 Database<br>جستجوی کاربر]
    
    %% ===============================
    %% اعتبارسنجی کاربر و رمز
    %% ===============================
    G --> H{👤 کاربر موجود است؟}
    H -->|خیر ❌| I[⚠️ خطا: کاربر یافت نشد]
    H -->|بله ✅| J{🔑 رمز عبور تنظیم شده؟}
    
    J -->|خیر ❌| K[⚠️ خطا: رمز تنظیم نشده]
    J -->|بله ✅| L{🔒 رمز عبور صحیح است؟}
    
    L -->|خیر ❌| M[⚠️ خطا: رمز اشتباه]
    L -->|بله ✅| N[🔐 JWT Service<br>تولید access_token و refresh_token]
    
    %% ===============================
    %% پاسخ موفق
    %% ===============================
    N --> O[✅ پاسخ موفق<br>+ access_token + refresh_token]
    
    %% ===============================
    %% مسیرهای خطا
    %% ===============================
    E --> P[❌ پاسخ خطا: محدودیت]
    I --> Q[❌ پاسخ خطا: اطلاعات اشتباه]
    K --> Q
    M --> Q

    %% ===============================
    %% استایل‌ها
    %% ===============================
    style A fill:#e3f2fd,stroke:#42a5f5,stroke-width:2px,stroke-dasharray: 4 2
    style B fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style C fill:#fff9c4,stroke:#fbc02d,stroke-width:2px
    style D fill:#c5cae9,stroke:#5c6bc0,stroke-width:2px
    style F fill:#d1c4e9,stroke:#7e57c2,stroke-width:2px
    style G fill:#e1bee7,stroke:#ab47bc,stroke-width:2px
    style H fill:#ffe0b2,stroke:#ffb74d,stroke-width:2px,stroke-dasharray: 2 2
    style J fill:#fff9c4,stroke:#fdd835,stroke-width:2px,stroke-dasharray: 2 2
    style L fill:#ffe0b2,stroke:#ffb74d,stroke-width:2px,stroke-dasharray: 2 2
    style N fill:#b3e5fc,stroke:#039be5,stroke-width:2px
    style O fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style P fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style Q fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style E fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style I fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style K fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style M fill:#ffcdd2,stroke:#c62828,stroke-width:2px
```

## 6. فلو خروج کاربر

این فلو برای خروج کاربر و ابطال توکن‌ها استفاده می‌شود.

```
flowchart TD
    %% ===============================
    %% کلاینت و درخواست خروج
    %% ===============================
    A[💻 کلاینت<br>درخواست خروج] --> B[🛠️ LogoutAPIView]
    
    %% ===============================
    %% بررسی احراز هویت
    %% ===============================
    B --> C{🔒 بررسی احراز هویت}
    C -->|معتبر ✅| D[🔑 AuthService<br>logout_user]
    C -->|نامعتبر ❌| E[⚠️ خطا: احراز هویت نشده]
    
    %% ===============================
    %% بررسی refresh token
    %% ===============================
    D --> F[🔐 JWT Service<br>بررسی refresh_token]
    F --> G{🔑 توکن معتبر است؟}
    
    G -->|بله ✅| H[🗂️ Token Blacklist<br>اضافه به لیست سیاه]
    G -->|خیر ❌| I[⚠️ خطا: توکن نامعتبر]
    
    %% ===============================
    %% پاسخ موفق
    %% ===============================
    H --> J[✅ پاسخ موفق<br>با موفقیت خارج شدید]
    
    %% ===============================
    %% مسیر خطا
    %% ===============================
    E --> K[❌ پاسخ خطا: احراز هویت]
    I --> L[❌ پاسخ خطا: توکن نامعتبر]

    %% ===============================
    %% استایل‌ها
    %% ===============================
    style A fill:#e3f2fd,stroke:#42a5f5,stroke-width:2px,stroke-dasharray: 4 2
    style B fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style C fill:#fff9c4,stroke:#fbc02d,stroke-width:2px
    style D fill:#c8e6c9,stroke:#43a047,stroke-width:2px
    style F fill:#d1c4e9,stroke:#7e57c2,stroke-width:2px
    style G fill:#ffe0b2,stroke:#ffb74d,stroke-width:2px,stroke-dasharray: 2 2
    style H fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style J fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style K fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style L fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style E fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style I fill:#ffcdd2,stroke:#c62828,stroke-width:2px
```

## 7. فلو تجدید توکن

این فلو برای تجدید access token با استفاده از refresh token استفاده می‌شود.

```
flowchart TD
    %% ===============================
    %% کلاینت و درخواست تجدید توکن
    %% ===============================
    A[💻 کلاینت<br>درخواست تجدید توکن] --> B[🛠️ CustomTokenRefreshView]
    
    %% ===============================
    %% بررسی Rate Limiting
    %% ===============================
    B --> C{⏱️ بررسی Rate Limiting}
    C -->|موفق ✅| D[🔐 SimpleJWT<br>اعتبارسنجی refresh_token]
    C -->|ناموفق ❌| E[⚠️ خطا: محدودیت درخواست]
    
    %% ===============================
    %% بررسی لیست سیاه
    %% ===============================
    D --> F[🗂️ Token Blacklist<br>بررسی لیست سیاه]
    F --> G{🔑 توکن فعال است؟}
    
    G -->|بله ✅| H[🔐 تولید access_token جدید]
    G -->|خیر ❌| I[⚠️ خطا: توکن در لیست سیاه یا منقضی]
    
    %% ===============================
    %% پاسخ موفق
    %% ===============================
    H --> J[✅ پاسخ موفق<br>+ access_token جدید]
    
    %% ===============================
    %% مسیر خطا
    %% ===============================
    E --> K[❌ پاسخ خطا: محدودیت]
    I --> L[❌ پاسخ خطا: توکن نامعتبر]

    %% ===============================
    %% استایل‌ها
    %% ===============================
    style A fill:#e3f2fd,stroke:#42a5f5,stroke-width:2px,stroke-dasharray: 4 2
    style B fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style C fill:#fff9c4,stroke:#fbc02d,stroke-width:2px
    style D fill:#c5cae9,stroke:#5c6bc0,stroke-width:2px
    style F fill:#d1c4e9,stroke:#7e57c2,stroke-width:2px
    style G fill:#ffe0b2,stroke:#ffb74d,stroke-width:2px,stroke-dasharray: 2 2
    style H fill:#c8e6c9,stroke:#43a047,stroke-width:2px
    style J fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style K fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style L fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style E fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style I fill:#ffcdd2,stroke:#c62828,stroke-width:2px
```

## 8. فلو کامل احراز هویت (جامع)

این نمودار فلو کامل احراز هویت از ابتدا تا انتها را نشان می‌دهد.

```
flowchart TD
    %% ===============================
    %% شروع جریان احراز هویت
    %% ===============================
    A[🚀 شروع: کاربر وارد identity می‌کند] --> B{📌 نوع identity}
    
    %% ===============================
    %% بررسی نوع identity
    %% ===============================
    B -->|📧 ایمیل| C[🔍 بررسی وجود کاربر با ایمیل]
    B -->|📱 شماره تلفن| D[🔍 بررسی وجود کاربر با تلفن]
    
    C -->|موجود ✅| E[✉️ ارسال کد OTP به ایمیل]
    C -->|جدید 🆕| F[🔗 ارسال لینک تایید به ایمیل]
    
    D -->|موجود ✅| G[📲 ارسال کد OTP به تلفن]
    D -->|جدید 🆕| H[📲 ارسال کد OTP به تلفن]
    
    %% ===============================
    %% ورود کد یا کلیک روی لینک
    %% ===============================
    E --> I[📝 کاربر کد OTP وارد می‌کند]
    F --> J[🔗 کاربر روی لینک کلیک می‌کند]
    G --> I
    H --> I
    
    %% ===============================
    %% اعتبارسنجی
    %% ===============================
    I --> K{✅ اعتبارسنجی کد}
    J --> L{✅ اعتبارسنجی لینک}
    
    K -->|معتبر ✅| M[🔑 ورود/ثبت‌نام کاربر]
    K -->|نامعتبر ❌| N[⚠️ نمایش خطا]
    
    L -->|معتبر ✅| O[🔑 ثبت‌نام کاربر جدید]
    L -->|نامعتبر ❌| N
    
    %% ===============================
    %% تولید توکن و پاسخ
    %% ===============================
    M --> P[🔐 تولید JWT Tokens]
    O --> P
    
    P --> Q[✅ پاسخ موفق<br>+ توکن‌ها]
    N --> R[❌ پاسخ خطا]
    
    %% ===============================
    %% نتیجه نهایی
    %% ===============================
    Q --> S[🎉 کاربر وارد سیستم شد]
    R --> T[🔁 کاربر مجدد تلاش می‌کند]
    
    T --> A

    %% ===============================
    %% استایل‌ها
    %% ===============================
    style A fill:#e1f5fe,stroke:#0288d1,stroke-width:2px,stroke-dasharray: 4 2
    style B fill:#fff9c4,stroke:#fbc02d,stroke-width:2px
    style C fill:#d1c4e9,stroke:#7e57c2,stroke-width:2px
    style D fill:#d1c4e9,stroke:#7e57c2,stroke-width:2px
    style E fill:#c8e6c9,stroke:#43a047,stroke-width:2px
    style F fill:#b2dfdb,stroke:#26a69a,stroke-width:2px
    style G fill:#c8e6c9,stroke:#43a047,stroke-width:2px
    style H fill:#b2dfdb,stroke:#26a69a,stroke-width:2px
    style I fill:#fff9c4,stroke:#fdd835,stroke-width:2px
    style J fill:#fff9c4,stroke:#fdd835,stroke-width:2px
    style K fill:#ffe0b2,stroke:#ffb74d,stroke-width:2px,stroke-dasharray: 2 2
    style L fill:#ffe0b2,stroke:#ffb74d,stroke-width:2px,stroke-dasharray: 2 2
    style M fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style O fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style P fill:#b3e5fc,stroke:#039be5,stroke-width:2px
    style Q fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style R fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style N fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style S fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style T fill:#ffe0b2,stroke:#ffb74d,stroke-width:2px
```

## 9. فلو مدیریت کش و Rate Limiting

این نمودار نحوه مدیریت کش و محدودیت‌های نرخ درخواست را نشان می‌دهد.

```
flowchart TD
    %% ===============================
    %% درخواست API و بررسی Rate Limiting
    %% ===============================
    A[🌐 درخواست API] --> B{⏱️ بررسی Rate Limiting}
    
    B -->|مجاز ✅| C[⚙️ ادامه پردازش]
    B -->|محدود ❌| D[❌ خطای 429: Too Many Requests]
    
    %% ===============================
    %% نوع عملیات
    %% ===============================
    C --> E{📌 نوع عملیات}
    
    E -->|📧 ارسال OTP/لینک| F[⏱️ بررسی Resend Cooldown]
    E -->|🔑 تایید کد| G[💾 بررسی OTP در کش]
    E -->|⚙️ سایر| H[ادامه عملیات عادی]
    
    %% ===============================
    %% مسیر ارسال OTP/لینک
    %% ===============================
    F -->|مجاز ✅| I[✉️/📲 ارسال کد/لینک]
    F -->|در cooldown ❌| J[⚠️ خطای انتظار]
    
    I --> M[⏱️ تنظیم Cooldown جدید]
    M --> P[💾 ذخیره در کش]
    P --> R[✅ پاسخ موفق]
    
    %% ===============================
    %% مسیر اعتبارسنجی OTP
    %% ===============================
    G -->|موجود ✅| K[🔑 اعتبارسنجی کد]
    G -->|منقضی ❌| L[⚠️ خطای انقضا]
    
    K -->|صحیح ✅| N[🗑️ حذف از کش]
    K -->|اشتباه ❌| O[⚠️ خطای کد نادرست]
    
    N --> Q[⚙️ ادامه فرآیند]
    Q --> S[🔐 تولید توکن‌ها]

    %% ===============================
    %% استایل‌ها
    %% ===============================
    style D fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style J fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style L fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style O fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style R fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style S fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style A fill:#e1f5fe,stroke:#0288d1,stroke-width:2px,stroke-dasharray: 4 2
    style B fill:#fff9c4,stroke:#fbc02d,stroke-width:2px
    style C fill:#d1c4e9,stroke:#7e57c2,stroke-width:2px
    style E fill:#fff9c4,stroke:#fdd835,stroke-width:2px
    style F fill:#ffe0b2,stroke:#ffb74d,stroke-width:2px
    style G fill:#d1c4e9,stroke:#7e57c2,stroke-width:2px
    style H fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style I fill:#c8e6c9,stroke:#43a047,stroke-width:2px
    style K fill:#b2dfdb,stroke:#26a69a,stroke-width:2px
    style M fill:#b3e5fc,stroke:#039be5,stroke-width:2px
    style N fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style P fill:#b3e5fc,stroke:#039be5,stroke-width:2px
    style Q fill:#dcedc8,stroke:#7cb342,stroke-width:2px
```
