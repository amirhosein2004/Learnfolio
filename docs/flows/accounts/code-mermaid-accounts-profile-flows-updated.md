# فلوهای مدیریت پروفایل - Accounts App

این سند شامل کد های نمودارهای ساده فلوهای مدیریت پروفایل کاربران و ادمین در سیستم Learnfolio است.

## 1. فلو مشاهده و ویرایش پروفایل کاربر

```
flowchart TD
    %% ===============================
    %% شروع فرآیند مدیریت پروفایل
    %% ===============================
    A[👤 کلاینت: درخواست پروفایل کاربر] --> B[🛠️ UserProfileAPIView]
    B --> C{🔍 نوع درخواست}
    
    %% ===============================
    %% مسیر GET, PATCH, DELETE
    %% ===============================
    C -->|GET| D[📄 نمایش پروفایل]
    C -->|PATCH| E[✏️ ویرایش نام]
    C -->|DELETE| F[🗑️ حذف حساب]
    
    %% ===============================
    %% سریالایز و اعتبارسنجی
    %% ===============================
    D --> G[📦 UserProfileSerializer: سریالایز اطلاعات]
    
    E --> H{🛡️ بررسی احراز هویت}
    F --> I{🛡️ بررسی احراز هویت}
    
    H -->|✅ معتبر| J[🕵️ UserFullNameSerializer: اعتبارسنجی نام]
    H -->|❌ نامعتبر| K[⚠️ خطا: احراز هویت]
    
    I -->|✅ معتبر| L[🛠️ ProfileService: حذف حساب]
    I -->|❌ نامعتبر| K
    
    %% ===============================
    %% به‌روزرسانی پایگاه داده
    %% ===============================
    J --> M[💾 Database: به‌روزرسانی نام]
    L --> N[💾 Database: حذف کاربر]
    
    %% ===============================
    %% پاسخ موفق
    %% ===============================
    G --> O[✅ پاسخ: اطلاعات پروفایل]
    M --> P[✅ پاسخ موفق: نام تغییر کرد]
    N --> Q[✅ پاسخ موفق: حساب حذف شد]
    
    %% ===============================
    %% مسیر خطا
    %% ===============================
    K --> R[❌ پاسخ خطا: دسترسی مجاز نیست]
    
    %% ===============================
    %% استایل‌ها
    %% ===============================
    style A fill:#e3f2fd,stroke:#42a5f5,stroke-width:2px
    style B fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style C fill:#fff59d,stroke:#fbc02d,stroke-width:2px
    style D fill:#c5cae9,stroke:#5c6bc0,stroke-width:2px
    style E fill:#c5cae9,stroke:#5c6bc0,stroke-width:2px
    style F fill:#c5cae9,stroke:#5c6bc0,stroke-width:2px
    style G fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style H fill:#fff9c4,stroke:#fdd835,stroke-width:2px
    style I fill:#fff9c4,stroke:#fdd835,stroke-width:2px
    style J fill:#d1c4e9,stroke:#7e57c2,stroke-width:2px
    style K fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style L fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style M fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style N fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style O fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style P fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style Q fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style R fill:#ffcdd2,stroke:#c62828,stroke-width:2px
```

## 2. فلو مدیریت پروفایل ادمین

```
flowchart TD
    %% ===============================
    %% شروع فرآیند مدیریت پروفایل ادمین
    %% ===============================
    A[👤 کلاینت ادمین: درخواست پروفایل] --> B[🛠️ AdminProfileAPIView]
    B --> C{🛡️ بررسی دسترسی ادمین}
    C -->|✅ مجاز| D{🔍 نوع درخواست}
    C -->|❌ غیرمجاز| E[⚠️ خطا: دسترسی ادمین ندارید]
    
    %% ===============================
    %% مسیر GET / PATCH
    %% ===============================
    D -->|GET| F[📄 AdminProfile.objects.get]
    D -->|PATCH| G[✏️ ویرایش پروفایل ادمین]
    
    F --> H[📦 AdminProfileSerializer: سریالایز]
    G --> I[🕵️ AdminProfileSerializer: اعتبارسنجی]
    
    I --> J[💾 Database: به‌روزرسانی پروفایل ادمین]
    J --> K[✅ پاسخ موفق: پروفایل ادمین به‌روزرسانی شد]
    
    H --> L[✅ پاسخ: اطلاعات پروفایل ادمین]
    E --> M[❌ پاسخ خطا: Forbidden]
    
    %% ===============================
    %% استایل‌ها
    %% ===============================
    style A fill:#e3f2fd,stroke:#42a5f5,stroke-width:2px
    style B fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style C fill:#fff59d,stroke:#fbc02d,stroke-width:2px
    style D fill:#fff9c4,stroke:#fdd835,stroke-width:2px
    style E fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style F fill:#c5cae9,stroke:#5c6bc0,stroke-width:2px
    style G fill:#c5cae9,stroke:#5c6bc0,stroke-width:2px
    style H fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style I fill:#d1c4e9,stroke:#7e57c2,stroke-width:2px
    style J fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style K fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style L fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style M fill:#ffcdd2,stroke:#c62828,stroke-width:2px
```

## 3. فلو درخواست تغییر ایمیل/تلفن

```
flowchart TD
    %% ===============================
    %% شروع فرآیند تغییر شناسه کاربر
    %% ===============================
    A[👤 کلاینت: درخواست تغییر شناسه] --> B[🛠️ UserUpdateEmailOrPhoneAPIView]
    B --> C{🛡️ بررسی احراز هویت}
    C -->|✅ معتبر| D[🕵️ UserPhoneOrEmailUpdateSerializer]
    C -->|❌ نامعتبر| E[⚠️ خطا: احراز هویت]
    
    %% ===============================
    %% پردازش و بررسی یکتایی
    %% ===============================
    D --> F[🔧 ProfileService: handle_identity_update]
    F --> G[🔍 ValidationService: بررسی یکتایی]
    
    G --> H{⚠️ شناسه تکراری است؟}
    H -->|✅ بله| I[❌ خطا: شناسه تکراری]
    H -->|❌ خیر| J{📧📱 نوع شناسه}
    
    %% ===============================
    %% ارسال کد یا لینک
    %% ===============================
    J -->|ایمیل| K[✉️ AuthService: ارسال لینک تایید]
    J -->|تلفن| L[📱 AuthService: ارسال کد OTP]
    
    K --> M[📧 send_email_task: ارسال لینک]
    L --> N[📱 send_sms_task: ارسال کد]
    
    M --> O[⏱️ تنظیم Cooldown]
    N --> O
    
    O --> P[✅ پاسخ موفق: کد/لینک ارسال شد]
    
    %% ===============================
    %% مسیرهای خطا
    %% ===============================
    E --> Q[❌ پاسخ خطا: احراز هویت]
    I --> R[❌ پاسخ خطا: شناسه تکراری]
    
    %% ===============================
    %% استایل‌ها
    %% ===============================
    style A fill:#e3f2fd,stroke:#42a5f5,stroke-width:2px
    style B fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style C fill:#fff59d,stroke:#fbc02d,stroke-width:2px
    style D fill:#d1c4e9,stroke:#7e57c2,stroke-width:2px
    style E fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style F fill:#b3e5fc,stroke:#039be5,stroke-width:2px
    style G fill:#fff9c4,stroke:#fdd835,stroke-width:2px
    style H fill:#fff9c4,stroke:#fdd835,stroke-width:2px
    style I fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style J fill:#fff59d,stroke:#fbc02d,stroke-width:2px
    style K fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style L fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style M fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style N fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style O fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style P fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style Q fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style R fill:#ffcdd2,stroke:#c62828,stroke-width:2px
```

## 4. فلو تایید تغییر شماره تلفن

```
flowchart TD
    %% ===============================
    %% شروع فرآیند تایید شماره تلفن
    %% ===============================
    A[📱 کلاینت: ارسال کد تایید تلفن] --> B[🛠️ VerifyOTPUserUpdatePhoneAPIView]
    B --> C{🛡️ بررسی احراز هویت}
    C -->|✅ معتبر| D[🕵️ VerifyOTPUserPhoneUpdateSerializer]
    C -->|❌ نامعتبر| E[⚠️ خطا: احراز هویت]
    
    %% ===============================
    %% بررسی کد OTP
    %% ===============================
    D --> F[🔍 ValidationService: بررسی کد OTP]
    F --> G[📦 Redis Cache: جستجوی کد]
    
    G --> H{⚠️ کد معتبر است؟}
    H -->|✅ بله| I[🗑️ حذف کد از کش]
    H -->|❌ خیر| J[❌ خطا: کد نامعتبر]
    
    I --> K[💾 Database: به‌روزرسانی شماره تلفن]
    K --> L[✅ پاسخ موفق: تلفن تغییر کرد]
    
    %% ===============================
    %% مسیرهای خطا
    %% ===============================
    E --> M[❌ پاسخ خطا: احراز هویت]
    J --> N[❌ پاسخ خطا: کد اشتباه]
    
    %% ===============================
    %% استایل‌ها
    %% ===============================
    style A fill:#e3f2fd,stroke:#42a5f5,stroke-width:2px
    style B fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style C fill:#fff59d,stroke:#fbc02d,stroke-width:2px
    style D fill:#d1c4e9,stroke:#7e57c2,stroke-width:2px
    style E fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style F fill:#b3e5fc,stroke:#039be5,stroke-width:2px
    style G fill:#fff9c4,stroke:#fdd835,stroke-width:2px
    style H fill:#fff9c4,stroke:#fdd835,stroke-width:2px
    style I fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style J fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style K fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style L fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style M fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style N fill:#ffcdd2,stroke:#c62828,stroke-width:2px
```

## 5. فلو تایید تغییر ایمیل

```
flowchart TD
    %% ===============================
    %% شروع فرآیند تایید تغییر ایمیل
    %% ===============================
    A[📧 کلاینت: کلیک لینک تایید ایمیل] --> B[🛠️ ConfirmationLinkUserUpdateEmailAPIView]
    B --> C{🛡️ بررسی احراز هویت}
    C -->|✅ معتبر| D[🕵️ ConfirmationLinkEmailUpdateSerializer]
    C -->|❌ نامعتبر| E[⚠️ خطا: احراز هویت]
    
    %% ===============================
    %% بررسی توکن ایمیل
    %% ===============================
    D --> F[🔍 ValidationService: بررسی توکن ایمیل]
    F --> G{⚠️ توکن معتبر است؟}
    
    G -->|✅ بله| H[💾 Database: به‌روزرسانی ایمیل]
    G -->|❌ خیر| I[❌ خطا: توکن نامعتبر]
    
    H --> J[✅ پاسخ موفق: ایمیل تغییر کرد]
    
    %% ===============================
    %% مسیرهای خطا
    %% ===============================
    E --> K[❌ پاسخ خطا: احراز هویت]
    I --> L[❌ پاسخ خطا: توکن نامعتبر]
    
    %% ===============================
    %% استایل‌ها
    %% ===============================
    style A fill:#e3f2fd,stroke:#42a5f5,stroke-width:2px
    style B fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style C fill:#fff59d,stroke:#fbc02d,stroke-width:2px
    style D fill:#d1c4e9,stroke:#7e57c2,stroke-width:2px
    style E fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style F fill:#b3e5fc,stroke:#039be5,stroke-width:2px
    style G fill:#fff9c4,stroke:#fdd835,stroke-width:2px
    style H fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style I fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style J fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style K fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style L fill:#ffcdd2,stroke:#c62828,stroke-width:2px
```
