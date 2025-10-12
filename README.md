# Wikibuno - پیشنهاد دهنده کافه

یک سیستم پیشنهاد کافه هوشمند که بر اساس موقعیت جغرافیایی و ترجیحات کاربران، بهترین کافه‌ها را پیشنهاد می‌دهد.

## 🎯 ویژگی‌های اصلی

### 👥 مدیریت کاربران
- **ثبت‌نام و لاگین با شماره تلفن** - احراز هویت ساده و امن
- **پروفایل کاربری کامل** - اطلاعات شخصی، موقعیت مکانی، ترجیحات
- **سیستم امتیازدهی** - لایک و کامنت روی کافه‌ها

### ☕ مدیریت کافه‌ها
- **ثبت کافه توسط کاربران** - هر کاربر می‌تواند کافه جدید اضافه کند
- **اطلاعات کامل کافه** - آدرس، امکانات، ساعات کاری، منو
- **سیستم امتیازدهی خودکار** - محاسبه میانگین امتیاز از نظرات کاربران
- **مدیریت توسط صاحبان** - کنترل کامل صفحات کافه توسط مالکان

### 🗺️ پیشنهاد هوشمند
- **پیشنهاد بر اساس موقعیت** - کافه‌های نزدیک به کاربر
- **فیلتر بر اساس ترجیحات** - نوع کافه، امکانات، قیمت
- **جستجوی پیشرفته** - بر اساس نام، شهر، امکانات

## 🛠️ تکنولوژی‌های استفاده شده

- **Backend**: Django 4.2.25 + Django REST Framework
- **Database**: SQLite (قابل تغییر به PostgreSQL/MySQL)
- **Authentication**: شماره تلفن + Token Authentication
- **File Storage**: Local (قابل تغییر به AWS S3)
- **Image Processing**: Pillow
- **API**: RESTful APIs

## 📋 مدل‌های داده

### User & UserProfile
- احراز هویت با شماره تلفن
- اطلاعات شخصی و موقعیت مکانی
- ترجیحات کافه

### Cafe
- اطلاعات کامل کافه
- موقعیت جغرافیایی
- امکانات و ویژگی‌ها
- سیستم امتیازدهی

### CafeMenu
- منوی کافه با دسته‌بندی
- قیمت‌گذاری
- وضعیت موجودی

### Like & Comment
- سیستم لایک و کامنت
- امتیازدهی 1-5 ستاره
- تایید نظرات

## 🚀 نصب و راه‌اندازی

### پیش‌نیازها
- Python 3.8+
- pip
- virtualenv

### مراحل نصب

1. **کلون کردن پروژه**
```bash
git clone <repository-url>
cd wikibuno
```

2. **ایجاد Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# یا
venv\Scripts\activate     # Windows
```

3. **نصب Dependencies**
```bash
pip install -r requirements.txt
```

4. **تنظیم Environment Variables**
```bash
cp env.example .env
# فایل .env را ویرایش کنید
```

5. **اجرای Migration ها**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **ایجاد Superuser**
```bash
python manage.py createsuperuser
```

7. **اجرای سرور**
```bash
python manage.py runserver
```

## 📁 ساختار پروژه

```
wikibuno/
├── config/                 # تنظیمات Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── user/                   # اپلیکیشن کاربران
│   ├── models.py          # مدل User و UserProfile
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── buno/                   # اپلیکیشن کافه‌ها
│   ├── models.py          # مدل‌های Cafe, Menu, Like, Comment
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── media/                  # فایل‌های آپلود شده
├── static/                 # فایل‌های استاتیک
├── requirements.txt        # Dependencies
├── manage.py
└── README.md
```

## 🔧 تنظیمات

### Environment Variables
فایل `env.example` را کپی کرده و به `.env` تغییر نام دهید:

```bash
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database
پیش‌فرض: SQLite
برای تغییر به PostgreSQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'wikibuno_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 📱 API Endpoints

### Authentication
- `POST /api/auth/register/` - ثبت‌نام
- `POST /api/auth/login/` - لاگین
- `POST /api/auth/logout/` - خروج

### Cafes
- `GET /api/cafes/` - لیست کافه‌ها
- `POST /api/cafes/` - ایجاد کافه جدید
- `GET /api/cafes/{id}/` - جزئیات کافه
- `PUT /api/cafes/{id}/` - ویرایش کافه
- `DELETE /api/cafes/{id}/` - حذف کافه

### Recommendations
- `GET /api/recommendations/` - پیشنهادات بر اساس موقعیت
- `GET /api/search/` - جستجوی کافه‌ها

## 🧪 تست

```bash
python manage.py test
```

## 📊 ویژگی‌های آینده

- [ ] اپلیکیشن موبایل (React Native/Flutter)
- [ ] سیستم پرداخت آنلاین
- [ ] رزرو میز
- [ ] اعلان‌های Push
- [ ] تحلیل‌های پیشرفته
- [ ] سیستم وفاداری
- [ ] یکپارچه‌سازی با شبکه‌های اجتماعی

## 🤝 مشارکت

1. Fork کنید
2. Branch جدید ایجاد کنید (`git checkout -b feature/amazing-feature`)
3. تغییرات را commit کنید (`git commit -m 'Add amazing feature'`)
4. Branch را push کنید (`git push origin feature/amazing-feature`)
5. Pull Request ایجاد کنید

## 📄 مجوز

این پروژه تحت مجوز MIT منتشر شده است. فایل [LICENSE](LICENSE) را برای جزئیات بیشتر مطالعه کنید.

## 📞 تماس

- ایمیل: your-email@example.com
- تلگرام: @your-telegram
- لینکدین: [Your LinkedIn](https://linkedin.com/in/your-profile)

---

**ساخته شده با ❤️ برای جامعه کافه‌دوستان ایران**
