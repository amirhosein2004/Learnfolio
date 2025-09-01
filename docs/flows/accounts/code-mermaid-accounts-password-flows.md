# فلوهای مدیریت رمز عبور - Accounts App

این سند شامل کد های نمودارهای ساده فلوهای مدیریت رمز عبور در سیستم Learnfolio است.

## 1. فلو درخواست بازیابی رمز عبور

```
flowchart TD
    %% ===============================
    %% شروع فرآیند بازیابی رمز
    %% ===============================
    A[🌐 کلاینت: درخواست بازیابی رمز] --> B[🛠️ RequestPasswordResetAPIView]
    B --> C{🛡️ بررسی CAPTCHA}
    C -->|✅ معتبر| D[🕵️ IdentitySerializer: اعتبارسنجی]
    C -->|❌ نامعتبر| E[⚠️ خطا: CAPTCHA نامعتبر]
    
    %% ===============================
    %% مسیر سرویس رمز عبور
    %% ===============================
    D --> F[🔑 PasswordService: handle_password_reset]
    F --> G{📌 نوع شناسه}
    
    G -->|📧 ایمیل| H[🔍 بررسی وجود کاربر با ایمیل]
    G -->|📲 تلفن| I[🔍 بررسی وجود کاربر با تلفن]
    
    %% ===============================
    %% ارسال لینک/کد
    %% ===============================
    H --> J[✉️ send_email_task: ارسال لینک بازیابی]
    I --> K[📲 send_sms_task: ارسال کد OTP]
    
    J --> L[⏱️ تنظیم Cooldown 2 دقیقه]
    K --> L
    
    %% ===============================
    %% پاسخ به کلاینت
    %% ===============================
    L --> M[✅ پاسخ موفق: لینک/کد ارسال شد]
    E --> N[❌ پاسخ خطا: CAPTCHA نامعتبر]
    
    %% ===============================
    %% استایل‌ها
    %% ===============================
    style A fill:#e3f2fd,stroke:#42a5f5,stroke-width:2px
    style B fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style C fill:#fff59d,stroke:#fbc02d,stroke-width:2px
    style D fill:#c5cae9,stroke:#5c6bc0,stroke-width:2px
    style E fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style F fill:#d1c4e9,stroke:#7e57c2,stroke-width:2px
    style G fill:#fff9c4,stroke:#fdd835,stroke-width:2px
    style H fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style I fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style J fill:#b3e5fc,stroke:#039be5,stroke-width:2px
    style K fill:#b3e5fc,stroke:#039be5,stroke-width:2px
    style L fill:#fff9c4,stroke:#fbc02d,stroke-width:2px
    style M fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style N fill:#ffcdd2,stroke:#c62828,stroke-width:2px
```

## 2. فلو تایید کد OTP برای بازیابی رمز عبور

```
flowchart TD
    %% ===============================
    %% شروع فرآیند تایید OTP
    %% ===============================
    A[📲 کلاینت: ارسال کد OTP] --> B[🛠️ OTPVerificationPasswordResetAPIView]
    B --> C{🛡️ بررسی CAPTCHA}
    C -->|✅ معتبر| D[🕵️ ResetOTPVerificationSerializer]
    C -->|❌ نامعتبر| E[⚠️ خطا: CAPTCHA نامعتبر]
    
    %% ===============================
    %% بررسی کد OTP
    %% ===============================
    D --> F[🔍 ValidationService: بررسی کد OTP]
    F --> G[💾 Redis Cache: جستجوی کد]
    
    G --> H{✔️ کد معتبر است؟}
    H -->|✅ بله| I[🗑️ حذف کد از کش]
    H -->|❌ خیر| J[⚠️ خطا: کد نامعتبر]
    
    %% ===============================
    %% تولید reset_token
    %% ===============================
    I --> K[🔑 PasswordService: تولید reset_token]
    K --> L[⏱️ JWT: انقضا 30 دقیقه]
    L --> M[✅ پاسخ موفق: reset_token]
    
    %% ===============================
    %% مسیر خطا
    %% ===============================
    E --> N[❌ پاسخ خطا: CAPTCHA نامعتبر]
    J --> O[❌ پاسخ خطا: کد اشتباه]
    
    %% ===============================
    %% استایل‌ها
    %% ===============================
    style A fill:#e3f2fd,stroke:#42a5f5,stroke-width:2px
    style B fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style C fill:#fff59d,stroke:#fbc02d,stroke-width:2px
    style D fill:#c5cae9,stroke:#5c6bc0,stroke-width:2px
    style E fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style F fill:#d1c4e9,stroke:#7e57c2,stroke-width:2px
    style G fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style H fill:#fff9c4,stroke:#fdd835,stroke-width:2px
    style I fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style J fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style K fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style L fill:#b3e5fc,stroke:#039be5,stroke-width:2px
    style M fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style N fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style O fill:#ffcdd2,stroke:#c62828,stroke-width:2px
```

## 3. فلو تایید لینک برای بازیابی رمز عبور

```
flowchart TD
    %% ===============================
    %% شروع فرآیند تایید لینک ایمیل
    %% ===============================
    A[📧 کلاینت: کلیک لینک ایمیل] --> B[🛠️ LinkVerificationPasswordResetAPIView]
    B --> C{🛡️ بررسی CAPTCHA}
    C -->|✅ معتبر| D[🕵️ ResetPasswordConfirmationLinkSerializer]
    C -->|❌ نامعتبر| E[⚠️ خطا: CAPTCHA نامعتبر]
    
    %% ===============================
    %% بررسی توکن ایمیل
    %% ===============================
    D --> F[🔍 ValidationService: بررسی توکن ایمیل]
    F --> G{✔️ توکن معتبر است؟}
    
    G -->|✅ بله| H[🔑 PasswordService: تولید reset_token]
    G -->|❌ خیر| I[⚠️ خطا: توکن نامعتبر]
    
    %% ===============================
    %% تولید reset_token
    %% ===============================
    H --> J[⏱️ JWT: انقضا 30 دقیقه]
    J --> K[✅ پاسخ موفق: reset_token]
    
    %% ===============================
    %% مسیر خطا
    %% ===============================
    E --> L[❌ پاسخ خطا: CAPTCHA نامعتبر]
    I --> M[❌ پاسخ خطا: توکن منقضی]
    
    %% ===============================
    %% استایل‌ها
    %% ===============================
    style A fill:#e3f2fd,stroke:#42a5f5,stroke-width:2px
    style B fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style C fill:#fff59d,stroke:#fbc02d,stroke-width:2px
    style D fill:#c5cae9,stroke:#5c6bc0,stroke-width:2px
    style E fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style F fill:#d1c4e9,stroke:#7e57c2,stroke-width:2px
    style G fill:#fff9c4,stroke:#fdd835,stroke-width:2px
    style H fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style I fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style J fill:#b3e5fc,stroke:#039be5,stroke-width:2px
    style K fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style L fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style M fill:#ffcdd2,stroke:#c62828,stroke-width:2px
```

## 4. فلو تنظیم رمز عبور جدید

```
flowchart TD
    %% ===============================
    %% شروع فرآیند تنظیم رمز جدید
    %% ===============================
    A[📲 کلاینت: ارسال رمز جدید] --> B[🛠️ ResetPasswordAPIView]
    B --> C{🛡️ بررسی CAPTCHA}
    C -->|✅ معتبر| D[🕵️ SetResetPasswordSerializer]
    C -->|❌ نامعتبر| E[⚠️ خطا: CAPTCHA نامعتبر]
    
    %% ===============================
    %% بررسی reset_token
    %% ===============================
    D --> F[🔍 ValidationService: بررسی reset_token]
    F --> G{✔️ توکن معتبر است؟}
    
    G -->|✅ بله| H[🔑 پیدا کردن کاربر]
    G -->|❌ خیر| I[⚠️ خطا: توکن منقضی]
    
    %% ===============================
    %% تطابق رمزهای جدید
    %% ===============================
    H --> J{🔒 تطابق رمزهای جدید}
    J -->|✅ بله| K[🛠️ PasswordService: تغییر رمز]
    J -->|❌ خیر| L[⚠️ خطا: رمزها مطابقت ندارند]
    
    %% ===============================
    %% ذخیره و پاسخ موفق
    %% ===============================
    K --> M[💾 Database: ذخیره رمز جدید]
    M --> N[✅ پاسخ موفق: رمز تغییر کرد]
    
    %% ===============================
    %% مسیر خطا
    %% ===============================
    E --> O[❌ پاسخ خطا: CAPTCHA نامعتبر]
    I --> P[❌ پاسخ خطا: توکن نامعتبر]
    L --> Q[❌ پاسخ خطا: عدم تطابق رمز]
    
    %% ===============================
    %% استایل‌ها
    %% ===============================
    style A fill:#e3f2fd,stroke:#42a5f5,stroke-width:2px
    style B fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style C fill:#fff59d,stroke:#fbc02d,stroke-width:2px
    style D fill:#c5cae9,stroke:#5c6bc0,stroke-width:2px
    style E fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style F fill:#d1c4e9,stroke:#7e57c2,stroke-width:2px
    style G fill:#fff9c4,stroke:#fdd835,stroke-width:2px
    style H fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style I fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style J fill:#fff9c4,stroke:#fdd835,stroke-width:2px
    style K fill:#b3e5fc,stroke:#039be5,stroke-width:2px
    style L fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style M fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style N fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style O fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style P fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style Q fill:#ffcdd2,stroke:#c62828,stroke-width:2px
```

## 5. فلو تنظیم رمز عبور برای اولین بار

```
flowchart TD
    %% ===============================
    %% شروع فرآیند تنظیم رمز جدید
    %% ===============================
    A[📲 کلاینت: ارسال رمز جدید] --> B[🛠️ FirstTimePasswordAPIView]
    B --> C{🛡️ بررسی CAPTCHA}
    C -->|✅ معتبر| D[🕵️ SetFirstTimePasswordSerializer]
    C -->|❌ نامعتبر| E[⚠️ خطا: CAPTCHA نامعتبر]
    
    %% ===============================
    %% بررسی reset_token
    %% ===============================
    D --> F[🔍 ValidationService: بررسی reset_token]
    F --> G{✔️ توکن معتبر است؟}
    
    G -->|✅ بله| H[🔑 پیدا کردن کاربر]
    G -->|❌ خیر| I[⚠️ خطا: توکن منقضی]
    
    %% ===============================
    %% تطابق رمزهای جدید
    %% ===============================
    H --> J{🔒 تطابق رمزهای جدید}
    J -->|✅ بله| K[🛠️ PasswordService: تغییر رمز]
    J -->|❌ خیر| L[⚠️ خطا: رمزها مطابقت ندارند]
    
    %% ===============================
    %% ذخیره و پاسخ موفق
    %% ===============================
    K --> M[💾 Database: ذخیره رمز جدید]
    M --> N[✅ پاسخ موفق: رمز تغییر کرد]
    
    %% ===============================
    %% مسیر خطا
    %% ===============================
    E --> O[❌ پاسخ خطا: CAPTCHA نامعتبر]
    I --> P[❌ پاسخ خطا: توکن نامعتبر]
    L --> Q[❌ پاسخ خطا: عدم تطابق رمز]
    
    %% ===============================
    %% استایل‌ها
    %% ===============================
    style A fill:#e3f2fd,stroke:#42a5f5,stroke-width:2px
    style B fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style C fill:#fff59d,stroke:#fbc02d,stroke-width:2px
    style D fill:#c5cae9,stroke:#5c6bc0,stroke-width:2px
    style E fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style F fill:#d1c4e9,stroke:#7e57c2,stroke-width:2px
    style G fill:#fff9c4,stroke:#fdd835,stroke-width:2px
    style H fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style I fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style J fill:#fff9c4,stroke:#fdd835,stroke-width:2px
    style K fill:#b3e5fc,stroke:#039be5,stroke-width:2px
    style L fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style M fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style N fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style O fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style P fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style Q fill:#ffcdd2,stroke:#c62828,stroke-width:2px
```

## 6. فلو تغییر رمز عبور

```
flowchart TD
    %% ===============================
    %% شروع فرآیند تغییر رمز موجود
    %% ===============================
    A[🔐 کلاینت: تغییر رمز موجود] --> B[🛠️ ChangePasswordAPIView]
    B --> C{🛡️ بررسی احراز هویت}
    C -->|✅ معتبر| D[🔍 HasPassword: بررسی وجود رمز]
    C -->|❌ نامعتبر| E[⚠️ خطا: احراز هویت]
    
    %% ===============================
    %% بررسی وجود رمز
    %% ===============================
    D --> F{🔒 کاربر رمز دارد؟}
    F -->|✅ دارد| G[🕵️ ChangePasswordSerializer]
    F -->|❌ ندارد| H[⚠️ خطا: رمز موجود نیست]
    
    %% ===============================
    %% بررسی رمز قدیم و تطابق رمز جدید
    %% ===============================
    G --> I{🔑 رمز قدیم صحیح است؟}
    I -->|✅ بله| J{🔒 تطابق رمزهای جدید}
    I -->|❌ خیر| K[⚠️ خطا: رمز قدیم اشتباه]
    
    J -->|✅ بله| L[🛠️ PasswordService: تغییر رمز]
    J -->|❌ خیر| M[⚠️ خطا: رمزها مطابقت ندارند]
    
    %% ===============================
    %% ذخیره و پاسخ موفق
    %% ===============================
    L --> N[💾 Database: ذخیره رمز جدید]
    N --> O[✅ پاسخ موفق: رمز تغییر کرد]
    
    %% ===============================
    %% مسیر خطا
    %% ===============================
    E --> P[❌ پاسخ خطا: احراز هویت]
    H --> Q[❌ پاسخ خطا: Forbidden]
    K --> R[❌ پاسخ خطا: رمز قدیم اشتباه]
    M --> S[❌ پاسخ خطا: عدم تطابق رمز]
    
    %% ===============================
    %% استایل‌ها
    %% ===============================
    style A fill:#e3f2fd,stroke:#42a5f5,stroke-width:2px
    style B fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style C fill:#fff59d,stroke:#fbc02d,stroke-width:2px
    style D fill:#c5cae9,stroke:#5c6bc0,stroke-width:2px
    style E fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style F fill:#fff9c4,stroke:#fdd835,stroke-width:2px
    style G fill:#d1c4e9,stroke:#7e57c2,stroke-width:2px
    style H fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style I fill:#fff9c4,stroke:#fdd835,stroke-width:2px
    style J fill:#fff9c4,stroke:#fdd835,stroke-width:2px
    style K fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style L fill:#b3e5fc,stroke:#039be5,stroke-width:2px
    style M fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style N fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style O fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style P fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style Q fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style R fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style S fill:#ffcdd2,stroke:#c62828,stroke-width:2px
```
