# فلوهای مدیریت مقالات - Blog App

این سند شامل  کد های نمودارهای ساده فلوهای مدیریت مقالات سیستم Learnfolio است که با استفاده از Mermaid.js ترسیم شده‌اند.

## 1. فلو ایجاد مقاله جدید

این فلو زمانی اجرا می‌شود که ادمین می‌خواهد مقاله جدیدی ایجاد کند.

```
flowchart TD
    %% ===============================
    %% شروع فرآیند ایجاد مقاله
    %% ===============================
    A[📝 ادمین: درخواست ایجاد مقاله] --> B[⚙️ BlogViewSet.create]
    B --> C{🛡️ بررسی احراز هویت و مجوز}
    C -->|✅ مجاز| D[📋 BlogSerializer: اعتبارسنجی داده‌ها]
    C -->|❌ غیرمجاز| E[🚫 خطا: دسترسی مجاز نیست]
    
    %% ===============================
    %% اعتبارسنجی
    %% ===============================
    D --> F{🔍 اعتبارسنجی موفق؟}
    F -->|✅ بله| G[🔑 بررسی یکتایی عنوان]
    F -->|❌ خیر| H[⚠️ خطا: داده‌های نامعتبر]
    
    %% ===============================
    %% بررسی یکتا بودن عنوان
    %% ===============================
    G --> I{📖 عنوان یکتا است؟}
    I -->|✅ بله| J[🖼️ بررسی اندازه تصویر]
    I -->|❌ خیر| K[⚠️ خطا: عنوان تکراری]
    
    %% ===============================
    %% بررسی تصویر
    %% ===============================
    J --> L{🖼️ تصویر معتبر است؟}
    L -->|✅ بله| M[✍️ perform_create: تنظیم نویسنده]
    L -->|❌ خیر| N[⚠️ خطا: تصویر نامعتبر]
    
    %% ===============================
    %% ذخیره مقاله
    %% ===============================
    M --> O[🔗 تولید slug خودکار]
    O --> P[💾 Database: ذخیره مقاله]
    P --> Q[🎉 پاسخ موفق: مقاله ایجاد شد]
    
    %% ===============================
    %% مسیر خطاها
    %% ===============================
    E --> R[❌ پاسخ خطا: 403 Forbidden]
    H --> S[❌ پاسخ خطا: 400 Bad Request]
    K --> T[❌ پاسخ خطا: عنوان تکراری]
    N --> U[❌ پاسخ خطا: تصویر نامعتبر]
    
    %% ===============================
    %% استایل‌ها
    %% ===============================
    style A fill:#e3f2fd,stroke:#42a5f5,stroke-width:2px
    style B fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style C fill:#fff59d,stroke:#fbc02d,stroke-width:2px
    style D fill:#c5cae9,stroke:#5c6bc0,stroke-width:2px
    style F fill:#d1c4e9,stroke:#7e57c2,stroke-width:2px
    style G fill:#ede7f6,stroke:#673ab7,stroke-width:2px
    style I fill:#ede7f6,stroke:#512da8,stroke-width:2px
    style J fill:#e1bee7,stroke:#8e24aa,stroke-width:2px
    style L fill:#e1bee7,stroke:#8e24aa,stroke-width:2px
    style M fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style O fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style P fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style Q fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    
    %% خطاها
    style E fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style H fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style K fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style N fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style R fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style S fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style T fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style U fill:#ffcdd2,stroke:#c62828,stroke-width:2px
```

## 2. فلو لیست مقالات با جستجو و صفحه‌بندی

این فلو برای نمایش لیست مقالات با قابلیت جستجو و صفحه‌بندی استفاده می‌شود.

```
flowchart TD
    %% ===============================
    %% شروع فرآیند
    %% ===============================
    A[🧑‍💻 کاربر: درخواست لیست مقالات] --> B[⚙️ BlogViewSet.list]
    B --> C[🔎 DjangoFilterBackend: اعمال فیلترها]
    C --> D[🔍 SearchFilter: جستجو در عنوان]
    
    %% ===============================
    %% بررسی پارامتر جستجو
    %% ===============================
    D --> E{📝 پارامترهای جستجو موجود است؟}
    E -->|✅ دارد| F[🔑 فیلتر بر اساس عنوان]
    E -->|❌ ندارد| G[📚 تمام مقالات]
    
    %% ===============================
    %% QuerySet
    %% ===============================
    F --> H[📂 QuerySet: مقالات فیلتر شده]
    G --> I[📂 QuerySet: تمام مقالات]
    
    H --> J[🗂️ مرتب‌سازی بر اساس تاریخ ایجاد]
    I --> J
    
    %% ===============================
    %% صفحه‌بندی و سریالایز
    %% ===============================
    J --> K[📑 BlogPagination: صفحه‌بندی]
    K --> L[📝 BlogSerializer: سریالایز داده‌ها]
    
    %% ===============================
    %% پاسخ نهایی
    %% ===============================
    L --> M[🎉 پاسخ موفق: لیست مقالات]
    
    %% ===============================
    %% استایل‌ها
    %% ===============================
    style A fill:#e3f2fd,stroke:#42a5f5,stroke-width:2px
    style B fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style C fill:#dcedc8,stroke:#689f38,stroke-width:2px
    style D fill:#f0f4c3,stroke:#afb42b,stroke-width:2px
    style E fill:#fff59d,stroke:#fbc02d,stroke-width:2px
    style F fill:#d1c4e9,stroke:#7e57c2,stroke-width:2px
    style G fill:#d1c4e9,stroke:#5e35b1,stroke-width:2px
    style H fill:#ede7f6,stroke:#4527a0,stroke-width:2px
    style I fill:#ede7f6,stroke:#311b92,stroke-width:2px
    style J fill:#c5cae9,stroke:#3949ab,stroke-width:2px
    style K fill:#ffe0b2,stroke:#f57c00,stroke-width:2px
    style L fill:#ffe0b2,stroke:#ef6c00,stroke-width:2px
    style M fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
```

## 3. فلو نمایش جزئیات مقاله

این فلو برای نمایش جزئیات یک مقاله خاص با استفاده از slug استفاده می‌شود.

```
flowchart TD
    %% ===============================
    %% شروع فرآیند
    %% ===============================
    A[🧑‍💻 کاربر: درخواست جزئیات مقاله] --> B[⚙️ BlogViewSet.retrieve]
    B --> C[🔑 lookup_field: جستجو با slug]
    
    %% ===============================
    %% بررسی موجودیت مقاله
    %% ===============================
    C --> D{📄 مقاله موجود است؟}
    D -->|✅ بله| E[📝 BlogSerializer: سریالایز مقاله]
    D -->|❌ خیر| F[⚠️ خطا: مقاله یافت نشد]
    
    %% ===============================
    %% پاسخ‌ها
    %% ===============================
    E --> G[🎉 پاسخ موفق: جزئیات مقاله]
    F --> H[🚨 پاسخ خطا: 404 Not Found]
    
    %% ===============================
    %% استایل‌ها
    %% ===============================
    style A fill:#e3f2fd,stroke:#42a5f5,stroke-width:2px
    style B fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style C fill:#f0f4c3,stroke:#afb42b,stroke-width:2px
    style D fill:#fff59d,stroke:#fbc02d,stroke-width:2px
    style E fill:#ffe0b2,stroke:#ef6c00,stroke-width:2px
    style F fill:#ffcdd2,stroke:#d32f2f,stroke-width:2px
    style G fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style H fill:#ffcdd2,stroke:#c62828,stroke-width:2px
```

## 4. فلو ویرایش مقاله

این فلو برای ویرایش مقاله توسط ادمین استفاده می‌شود.

```
flowchart TD
    %% ===============================
    %% شروع فرآیند
    %% ===============================
    A[🧑‍💼 ادمین: درخواست ویرایش مقاله] --> B[⚙️ BlogViewSet.update]
    B --> C{🔒 بررسی احراز هویت و مجوز}
    C -->|✅ مجاز| D[🔎 جستجو مقاله با slug]
    C -->|❌ غیرمجاز| E[🚫 خطا: دسترسی مجاز نیست]
    
    %% ===============================
    %% بررسی موجودیت
    %% ===============================
    D --> F{📄 مقاله موجود است؟}
    F -->|✅ بله| G[📝 BlogSerializer: اعتبارسنجی داده‌ها]
    F -->|❌ خیر| H[⚠️ خطا: مقاله یافت نشد]
    
    %% ===============================
    %% اعتبارسنجی داده‌ها
    %% ===============================
    G --> I{✅ اعتبارسنجی موفق؟}
    I -->|بله| J[🔍 بررسی یکتایی عنوان جدید]
    I -->|خیر| K[❌ خطا: داده‌های نامعتبر]
    
    %% ===============================
    %% بررسی عنوان
    %% ===============================
    J --> L{📑 عنوان یکتا است؟}
    L -->|بله| M[🖼️ بررسی تصویر جدید]
    L -->|خیر| N[⚠️ خطا: عنوان تکراری]
    
    %% ===============================
    %% بررسی تصویر
    %% ===============================
    M --> O{🖼️ تصویر معتبر است؟}
    O -->|بله| P[🔗 به‌روزرسانی slug در صورت تغییر عنوان]
    O -->|خیر| Q[🚫 خطا: تصویر نامعتبر]
    
    %% ===============================
    %% عملیات نهایی
    %% ===============================
    P --> R[💾 Database: به‌روزرسانی مقاله]
    R --> S[🎉 پاسخ موفق: مقاله ویرایش شد]
    
    %% ===============================
    %% پاسخ‌های خطا
    %% ===============================
    E --> T[🚨 پاسخ خطا: 403 Forbidden]
    H --> U[🚨 پاسخ خطا: 404 Not Found]
    K --> V[🚨 پاسخ خطا: 400 Bad Request]
    N --> W[🚨 پاسخ خطا: عنوان تکراری]
    Q --> X[🚨 پاسخ خطا: تصویر نامعتبر]
    
    %% ===============================
    %% استایل‌ها
    %% ===============================
    style A fill:#e3f2fd,stroke:#42a5f5,stroke-width:2px
    style B fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style C fill:#f0f4c3,stroke:#afb42b,stroke-width:2px
    style D fill:#fff9c4,stroke:#fbc02d,stroke-width:2px
    style F fill:#ffe082,stroke:#ffb300,stroke-width:2px
    style G fill:#ffe0b2,stroke:#ef6c00,stroke-width:2px
    style I fill:#fff59d,stroke:#fdd835,stroke-width:2px
    style J fill:#ffe082,stroke:#ffa000,stroke-width:2px
    style L fill:#ffecb3,stroke:#ffb300,stroke-width:2px
    style M fill:#d1c4e9,stroke:#673ab7,stroke-width:2px
    style O fill:#d1c4e9,stroke:#5e35b1,stroke-width:2px
    style P fill:#c5cae9,stroke:#3949ab,stroke-width:2px
    style R fill:#cfd8dc,stroke:#455a64,stroke-width:2px
    style S fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    
    style E fill:#ffcdd2,stroke:#d32f2f,stroke-width:2px
    style H fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style K fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style N fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style Q fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style T fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style U fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style V fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style W fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style X fill:#ffcdd2,stroke:#c62828,stroke-width:2px
```

## 5. فلو حذف مقاله

این فلو برای حذف مقاله توسط ادمین استفاده می‌شود.

```
flowchart TD
    %% ===============================
    %% شروع فرآیند
    %% ===============================
    A[🧑‍💼 ادمین: درخواست حذف مقاله] --> B[⚙️ BlogViewSet.destroy]
    B --> C{🔒 بررسی احراز هویت و مجوز}
    C -->|✅ مجاز| D[🔎 جستجو مقاله با slug]
    C -->|❌ غیرمجاز| E[🚫 خطا: دسترسی مجاز نیست]
    
    %% ===============================
    %% بررسی موجودیت
    %% ===============================
    D --> F{📄 مقاله موجود است؟}
    F -->|✅ بله| G[💾 Database: حذف مقاله]
    F -->|❌ خیر| H[⚠️ خطا: مقاله یافت نشد]
    
    %% ===============================
    %% عملیات نهایی
    %% ===============================
    G --> I[🎉 پاسخ موفق: مقاله حذف شد]
    
    %% ===============================
    %% پاسخ‌های خطا
    %% ===============================
    E --> J[🚨 پاسخ خطا: 403 Forbidden]
    H --> K[🚨 پاسخ خطا: 404 Not Found]
    
    %% ===============================
    %% استایل‌ها
    %% ===============================
    style A fill:#e3f2fd,stroke:#42a5f5,stroke-width:2px
    style B fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    style C fill:#f0f4c3,stroke:#afb42b,stroke-width:2px
    style D fill:#fff9c4,stroke:#fbc02d,stroke-width:2px
    style F fill:#ffe082,stroke:#ffb300,stroke-width:2px
    style G fill:#d7ccc8,stroke:#6d4c41,stroke-width:2px
    style I fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    
    style E fill:#ffcdd2,stroke:#d32f2f,stroke-width:2px
    style H fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style J fill:#ffcdd2,stroke:#c62828,stroke-width:2px
    style K fill:#ffcdd2,stroke:#c62828,stroke-width:2px
```

## 6. فلو کامل مدیریت مقالات

این نمودار فلو کامل مدیریت مقالات از ابتدا تا انتها را نشان می‌دهد.

```
flowchart TD
    %% ===============================
    %% شروع
    %% ===============================
    A[🚀 شروع: کاربر وارد بخش مقالات می‌شود] --> B{👤 نوع کاربر}
    
    %% ===============================
    %% کاربر عادی
    %% ===============================
    B -->|🙍 کاربر عادی| C[📚 مشاهده لیست مقالات]
    C --> E[📰 انتخاب مقاله]
    E --> F[🔎 مشاهده جزئیات مقاله]
    F --> T[🏁 پایان: مشاهده مقاله]
    
    %% ===============================
    %% ادمین
    %% ===============================
    B -->|🧑‍💼 ادمین| D{⚙️ نوع عملیات}
    
    D -->|➕ ایجاد| G[📝 فرم ایجاد مقاله]
    D -->|👁️ مشاهده| H[📋 لیست مقالات ادمین]
    D -->|✏️ ویرایش| I[🖊️ انتخاب مقاله برای ویرایش]
    D -->|🗑️ حذف| J[🗑️ انتخاب مقاله برای حذف]
    
    %% --- ایجاد ---
    G --> K[✍️ پر کردن اطلاعات مقاله]
    K --> L[📤 ارسال درخواست ایجاد]
    L --> M[✅ مقاله ایجاد شد]
    M --> U[🏁 پایان: مقاله جدید ایجاد شد]
    
    %% --- مشاهده (ادمین) ---
    H --> N[📋 مشاهده لیست با امکان مدیریت]
    N --> T
    
    %% --- ویرایش ---
    I --> O[✏️ فرم ویرایش مقاله]
    O --> P[📤 ارسال تغییرات]
    P --> Q[✅ مقاله ویرایش شد]
    Q --> V[🏁 پایان: مقاله ویرایش شد]
    
    %% --- حذف ---
    J --> R[⚠️ تایید حذف]
    R --> S[🗑️ مقاله حذف شد]
    S --> W[🏁 پایان: مقاله حذف شد]
    
    %% ===============================
    %% استایل‌ها
    %% ===============================
    style A fill:#e3f2fd,stroke:#42a5f5,stroke-width:2px
    style B fill:#fff9c4,stroke:#fbc02d,stroke-width:2px
    style C fill:#f0f4c3,stroke:#afb42b,stroke-width:2px
    style D fill:#ffe082,stroke:#ffb300,stroke-width:2px
    style F fill:#d1c4e9,stroke:#5e35b1,stroke-width:2px
    style H fill:#bbdefb,stroke:#1e88e5,stroke-width:2px
    
    style M fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style Q fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style S fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style T fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style U fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style V fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style W fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
```
