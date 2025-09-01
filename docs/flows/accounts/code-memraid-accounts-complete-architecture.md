# معماری کامل سیستم Accounts - Learnfolio

این سند نمای کلی ساده از معماری و کد های فلوهای سیستم احراز هویت و مدیریت حساب‌های کاربری را ارائه می‌دهد.

## نمای کلی معماری

```
flowchart TD
    %% ===============================
    %% کلاینت و API Gateway
    %% ===============================
    A[💻 کلاینت: Frontend/Mobile App] --> B[🌐 API Gateway]
    B --> C{📌 نوع درخواست}
    
    %% ===============================
    %% مسیر درخواست‌ها
    %% ===============================
    C -->|🔑 احراز هویت| D[Authentication APIs]
    C -->|🔒 مدیریت رمز| E[Password Management APIs]
    C -->|👤 مدیریت پروفایل| F[Profile Management APIs]
    
    %% ===============================
    %% سرویس‌ها
    %% ===============================
    D --> G[🛠️ AuthService]
    E --> H[🛠️ PasswordService]
    F --> I[🛠️ ProfileService]
    
    G --> J[🕵️ ValidationService]
    H --> J
    I --> J
    
    %% ===============================
    %% Cache
    %% ===============================
    J --> K[⏱️ CacheService]
    K --> L[💾 Redis Cache]
    
    %% ===============================
    %% Database
    %% ===============================
    G --> M[💾 Database: PostgreSQL]
    H --> M
    I --> M
    
    %% ===============================
    %% Task Queue و سرویس‌های خارجی
    %% ===============================
    G --> N[⚡ Celery Tasks]
    H --> N
    I --> N
    
    N --> O[🌐 External Services]
    O --> P[✉️ Email Service]
    O --> Q[📲 SMS Service]
    
    %% ===============================
    %% استایل‌ها
    %% ===============================
    style A fill:#e3f2fd,stroke:#42a5f5,stroke-width:2px
    style B fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style C fill:#fff9c4,stroke:#fbc02d,stroke-width:2px
    style D fill:#c5cae9,stroke:#5c6bc0,stroke-width:2px
    style E fill:#c5cae9,stroke:#5c6bc0,stroke-width:2px
    style F fill:#c5cae9,stroke:#5c6bc0,stroke-width:2px
    style G fill:#d1c4e9,stroke:#7e57c2,stroke-width:2px
    style H fill:#d1c4e9,stroke:#7e57c2,stroke-width:2px
    style I fill:#d1c4e9,stroke:#7e57c2,stroke-width:2px
    style J fill:#fff9c4,stroke:#fdd835,stroke-width:2px
    style K fill:#fff3e0,stroke:#fb8c00,stroke-width:2px
    style L fill:#fff3e0,stroke:#fb8c00,stroke-width:2px
    style M fill:#c8e6c9,stroke:#43a047,stroke-width:2px
    style N fill:#d1c4e9,stroke:#7e57c2,stroke-width:2px
    style O fill:#f3e5f5,stroke:#8e24aa,stroke-width:2px
    style P fill:#f3e5f5,stroke:#8e24aa,stroke-width:2px
    style Q fill:#f3e5f5,stroke:#8e24aa,stroke-width:2px
```

## مدل‌های داده

```
erDiagram
    %% ===============================
    %% جدول کاربران
    %% ===============================
    User {
        int id PK "شناسه کاربر"
        string full_name "نام کامل"
        string email UK "ایمیل (منحصر به فرد)"
        string phone_number UK "شماره تلفن (منحصر به فرد)"
        boolean is_active "فعال/غیرفعال"
        boolean is_staff "کارمند/مدیر"
        datetime date_joined "تاریخ ثبت‌نام"
        datetime last_login "آخرین ورود"
        string password "رمز عبور هش شده"
    }
    
    %% ===============================
    %% پروفایل ادمین
    %% ===============================
    AdminProfile {
        int id PK "شناسه پروفایل"
        int user_id FK "شناسه کاربر مرتبط"
        json social_networks "شبکه‌های اجتماعی"
        text description "توضیحات"
        string image "تصویر پروفایل"
        datetime created_at "تاریخ ایجاد"
        datetime updated_at "تاریخ آخرین بروزرسانی"
    }
    
    %% ===============================
    %% ارتباط
    %% ===============================
    User ||--o| AdminProfile : "یک به یک (Admin Profile)"
```

## فلو کامل سیستم احراز هویت

```
flowchart TD
    %% ===============================
    %% شروع جریان ورود/ثبت‌نام
    %% ===============================
    A[🌐 کاربر وارد سایت می‌شود] --> B{❓ کاربر حساب دارد؟}
    
    B -->|✅ بله| C[🔑 ورود به سیستم]
    B -->|🆕 خیر| D[📝 ثبت‌نام جدید]
    
    %% ===============================
    %% مسیر ورود
    %% ===============================
    C --> E{📌 نحوه ورود}
    E -->|🔢 OTP| F[✉️/📲 ارسال کد به ایمیل/تلفن]
    E -->|🔒 رمز عبور| G[🛠️ وارد کردن رمز]
    
    %% ===============================
    %% مسیر ثبت‌نام
    %% ===============================
    D --> H[📧 وارد کردن ایمیل/تلفن]
    H --> I[✉️/📲 ارسال کد/لینک تایید]
    
    %% ===============================
    %% اعتبارسنجی
    %% ===============================
    F --> J[✅ تایید کد OTP]
    G --> K{🔑 رمز صحیح است؟}
    I --> L[✅ تایید هویت]
    
    K -->|✅ بله| M[🎉 ورود موفق]
    K -->|❌ خیر| N[⚠️ خطا: رمز اشتباه]
    J --> M
    L --> O[🎉 ثبت‌نام موفق]
    
    %% ===============================
    %% توکن‌ها و دسترسی
    %% ===============================
    M --> P[🔐 دریافت JWT Tokens]
    O --> P
    P --> Q[💻 دسترسی به سیستم]
    
    %% ===============================
    %% عملیات کاربر
    %% ===============================
    Q --> R{🛠️ عملیات کاربر}
    R -->|👤 مدیریت پروفایل| S[✏️ ویرایش اطلاعات]
    R -->|🔒 تغییر رمز| T[🛠️ مدیریت رمز عبور]
    R -->|🚪 خروج| U[🗝️ Logout]
    
    S --> V[✅ به‌روزرسانی موفق]
    T --> W[✅ رمز تغییر کرد]
    U --> X[✅ خروج از سیستم]
    
    %% ===============================
    %% استایل‌ها
    %% ===============================
    style A fill:#e3f2fd,stroke:#42a5f5,stroke-width:2px
    style B fill:#fff9c4,stroke:#fbc02d,stroke-width:2px
    style C fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style D fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style E fill:#fff9c4,stroke:#fdd835,stroke-width:2px
    style F fill:#c8e6c9,stroke:#43a047,stroke-width:2px
    style G fill:#c8e6c9,stroke:#43a047,stroke-width:2px
    style H fill:#b2dfdb,stroke:#26a69a,stroke-width:2px
    style I fill:#b2dfdb,stroke:#26a69a,stroke-width:2px
    style J fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style K fill:#ffe0b2,stroke:#ffb74d,stroke-width:2px
    style L fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style M fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style N fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style O fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style P fill:#b3e5fc,stroke:#039be5,stroke-width:2px
    style Q fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style R fill:#fff9c4,stroke:#fdd835,stroke-width:2px
    style S fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style T fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style U fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style V fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style W fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style X fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
```

## نقشه API Endpoints

```
mindmap
  root((Accounts API))
    Authentication
      submit-identity/
        POST: ارسال ایمیل/تلفن
      verify-otp/
        POST: تایید کد OTP
      verify-link/
        POST: تایید لینک ایمیل
      resend-otp-or-link/
        POST: ارسال مجدد
      login-password/
        POST: ورود با رمز
      logout/
        POST: خروج
      token/refresh/
        POST: تجدید توکن
    
    Password Management
      request-reset/
        POST: درخواست بازیابی
      verify-otp/
        POST: تایید کد بازیابی
      verify-link/
        POST: تایید لینک بازیابی
      reset/
        POST: تنظیم رمز جدید
      first-time/
        POST: اولین رمز
      change/
        PATCH: تغییر رمز
    
    Profile Management
      user/
        GET: مشاهده پروفایل
        PATCH: ویرایش نام
        DELETE: حذف حساب
      admin/
        GET: مشاهده پروفایل ادمین
        PATCH: ویرایش پروفایل ادمین
      update-identity/
        PATCH: درخواست تغییر شناسه
      verify-phone-update/
        PATCH: تایید تغییر تلفن
      confirm-email-update/
        PATCH: تایید تغییر ایمیل
```

## لایه‌های امنیتی

```
flowchart TD
    %% ===============================
    %% جریان پردازش درخواست کاربر
    %% ===============================
    A[🌐 درخواست کاربر] --> B[🛡️ CAPTCHA: Cloudflare Turnstile]
    B --> C[⏱️ Rate Limiting: محدودیت درخواست]
    C --> D[🔑 Authentication: JWT Token]
    D --> E[🛠️ Permission: بررسی دسترسی]
    E --> F[🕵️ Validation: اعتبارسنجی داده‌ها]
    F --> G[💼 Business Logic: منطق کسب‌وکار]
    G --> H[💾 Database: عملیات پایگاه داده]
    H --> I[📤 Response: پاسخ به کاربر]
    
    %% ===============================
    %% استایل‌ها
    %% ===============================
    style A fill:#e3f2fd,stroke:#42a5f5,stroke-width:2px
    style B fill:#fff59d,stroke:#fbc02d,stroke-width:2px
    style C fill:#ffcc80,stroke:#fb8c00,stroke-width:2px
    style D fill:#ef9a9a,stroke:#d32f2f,stroke-width:2px
    style E fill:#ce93d8,stroke:#7b1fa2,stroke-width:2px
    style F fill:#7986cb,stroke:#303f9f,stroke-width:2px
    style G fill:#aed581,stroke:#558b2f,stroke-width:2px
    style H fill:#fff59d,stroke:#fbc02d,stroke-width:2px
    style I fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
```

## مدیریت کش و Session

```
flowchart TD
    %% ===============================
    %% شروع فرآیند OTP/Token
    %% ===============================
    A[📩 درخواست OTP/Link] --> B[🔑 تولید کد/توکن]
    B --> C[💾 ذخیره در Redis]
    C --> D[⏱️ تنظیم TTL]
    
    %% ===============================
    %% نوع کش و TTL
    %% ===============================
    D --> E{📌 نوع کش}
    E -->|🔢 OTP Code| F[⏱️ TTL: 2 دقیقه]
    E -->|⏱️ Resend Cooldown| G[⏱️ TTL: 2 دقیقه]
    E -->|📧 Email Token| H[⏱️ TTL: 15 دقیقه]
    E -->|🔑 Reset Token| I[⏱️ TTL: 30 دقیقه]
    
    %% ===============================
    %% مسیر کاربر
    %% ===============================
    F --> J[🕐 انتظار تایید کاربر]
    G --> K[🚫 جلوگیری از Spam]
    H --> L[✅ تایید ایمیل]
    I --> M[🔑 بازیابی رمز]
    
    J --> N{✔️ تایید شد؟}
    N -->|✅ بله| O[🗑️ حذف از کش]
    N -->|❌ خیر| P[⏳ انقضای خودکار]
    
    %% ===============================
    %% استایل‌ها
    %% ===============================
    style B fill:#ffeb3b,stroke:#fbc02d,stroke-width:2px
    style C fill:#4caf50,stroke:#2e7d32,stroke-width:2px
    style D fill:#fff59d,stroke:#fbc02d,stroke-width:2px
    style F fill:#ffe082,stroke:#ffa000,stroke-width:2px
    style G fill:#ffe082,stroke:#ffa000,stroke-width:2px
    style H fill:#fff59d,stroke:#fbc02d,stroke-width:2px
    style I fill:#fff59d,stroke:#fbc02d,stroke-width:2px
    style J fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style K fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style L fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style M fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style O fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style P fill:#ffcdd2,stroke:#c62828,stroke-width:2px
```
