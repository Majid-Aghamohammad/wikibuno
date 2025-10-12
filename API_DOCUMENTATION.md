# 📚 مستندات API - WikiBuno

## 🎯 معرفی

WikiBuno یک سیستم پیشنهاد کافه است که به کاربران امکان یافتن بهترین کافه‌ها بر اساس موقعیت مکانی، علایق و نظرات سایر کاربران را می‌دهد.

## 🔗 Base URL

```
http://localhost:8000/api/
```

## 🔐 احراز هویت

API از Token Authentication استفاده می‌کند. برای دسترسی به endpoint های محافظت شده، باید token را در header ارسال کنید:

```
Authorization: Token <your_token_here>
```

---

## 👤 API های کاربران

### 1. ثبت‌نام کاربر جدید

**Endpoint:** `POST /api/auth/register/`

**بدون احراز هویت**

**Request Body:**
```json
{
    "phone_number": "09123456789",
    "first_name": "علی",
    "last_name": "احمدی",
    "email": "ali@example.com",
    "password": "password123",
    "password_confirm": "password123"
}
```

**Response (201 Created):**
```json
{
    "message": "کاربر با موفقیت ثبت شد",
    "user": {
        "id": 1,
        "phone_number": "09123456789",
        "first_name": "علی",
        "last_name": "احمدی",
        "email": "ali@example.com",
        "username": "user_09123456789"
    },
    "token": "abc123def456..."
}
```

### 2. ورود کاربر

**Endpoint:** `POST /api/auth/login/`

**بدون احراز هویت**

**Request Body:**
```json
{
    "phone_number": "09123456789",
    "password": "password123"
}
```

**Response (200 OK):**
```json
{
    "message": "ورود موفقیت‌آمیز",
    "user": {
        "id": 1,
        "phone_number": "09123456789",
        "first_name": "علی",
        "last_name": "احمدی",
        "email": "ali@example.com"
    },
    "token": "abc123def456..."
}
```

### 3. خروج کاربر

**Endpoint:** `POST /api/auth/logout/`

**نیاز به احراز هویت**

**Response (200 OK):**
```json
{
    "message": "خروج موفقیت‌آمیز"
}
```

### 4. مشاهده پروفایل کاربر

**Endpoint:** `GET /api/auth/profile/`

**نیاز به احراز هویت**

**Response (200 OK):**
```json
{
    "id": 1,
    "phone_number": "09123456789",
    "first_name": "علی",
    "last_name": "احمدی",
    "email": "ali@example.com",
    "username": "user_09123456789"
}
```

### 5. ویرایش پروفایل کاربر

**Endpoint:** `PUT /api/auth/profile/`

**نیاز به احراز هویت**

**Request Body:**
```json
{
    "first_name": "علی",
    "last_name": "احمدی",
    "email": "ali.new@example.com"
}
```

**Response (200 OK):**
```json
{
    "id": 1,
    "phone_number": "09123456789",
    "first_name": "علی",
    "last_name": "احمدی",
    "email": "ali.new@example.com",
    "username": "user_09123456789"
}
```

### 6. مشاهده جزئیات پروفایل

**Endpoint:** `GET /api/auth/profile/detail/`

**نیاز به احراز هویت**

**Response (200 OK):**
```json
{
    "id": 1,
    "user": 1,
    "bio": "علاقه‌مند به کافه‌گردی",
    "avatar": null,
    "birth_date": "1990-01-01",
    "location": "تهران",
    "latitude": "35.6892",
    "longitude": "51.3890",
    "favorite_cafe_types": ["modern", "traditional"],
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:00:00Z"
}
```

### 7. ویرایش جزئیات پروفایل

**Endpoint:** `PUT /api/auth/profile/detail/`

**نیاز به احراز هویت**

**Request Body:**
```json
{
    "bio": "علاقه‌مند به کافه‌گردی و قهوه",
    "location": "تهران، ولیعصر",
    "latitude": "35.6892",
    "longitude": "51.3890",
    "favorite_cafe_types": ["modern", "traditional", "cozy"]
}
```

### 8. تغییر رمز عبور

**Endpoint:** `PUT /api/auth/change-password/`

**نیاز به احراز هویت**

**Request Body:**
```json
{
    "old_password": "oldpassword123",
    "new_password": "newpassword123",
    "new_password_confirm": "newpassword123"
}
```

**Response (200 OK):**
```json
{
    "message": "رمز عبور با موفقیت تغییر کرد"
}
```

### 9. داشبورد کاربر

**Endpoint:** `GET /api/auth/dashboard/`

**نیاز به احراز هویت**

**Response (200 OK):**
```json
{
    "user": {
        "id": 1,
        "phone_number": "09123456789",
        "first_name": "علی",
        "last_name": "احمدی"
    },
    "profile": {
        "id": 1,
        "bio": "علاقه‌مند به کافه‌گردی",
        "location": "تهران"
    },
    "stats": {
        "owned_cafes": 2,
        "cafe_likes": 15,
        "cafe_comments": 8
    }
}
```

### 10. به‌روزرسانی موقعیت مکانی

**Endpoint:** `POST /api/auth/update-location/`

**نیاز به احراز هویت**

**Request Body:**
```json
{
    "latitude": "35.6892",
    "longitude": "51.3890"
}
```

**Response (200 OK):**
```json
{
    "message": "موقعیت مکانی با موفقیت به‌روزرسانی شد"
}
```

---

## ☕ API های کافه‌ها

### 1. لیست کافه‌ها

**Endpoint:** `GET /api/cafes/`

**بدون احراز هویت**

**Query Parameters:**
- `page`: شماره صفحه (اختیاری)
- `page_size`: تعداد آیتم در هر صفحه (اختیاری)
- `search`: جستجو در نام کافه (اختیاری)
- `city`: فیلتر بر اساس شهر (اختیاری)
- `cafe_type`: فیلتر بر اساس نوع کافه (اختیاری)
- `has_wifi`: فیلتر بر اساس وجود وای‌فای (اختیاری)
- `has_parking`: فیلتر بر اساس وجود پارکینگ (اختیاری)

**Response (200 OK):**
```json
{
    "count": 25,
    "next": "http://localhost:8000/api/cafes/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "کافه مرکزی",
            "description": "کافه دنج در مرکز شهر",
            "cafe_type": "modern",
            "phone_number": "02112345678",
            "address": "تهران، خیابان ولیعصر",
            "city": "تهران",
            "latitude": "35.6892",
            "longitude": "51.3890",
            "capacity": 50,
            "has_wifi": true,
            "has_parking": true,
            "is_smoking_allowed": false,
            "has_outdoor_seating": true,
            "average_rating": 4.5,
            "total_reviews": 120,
            "main_image": "http://localhost:8000/media/cafes/cafe1.jpg",
            "gallery": ["http://localhost:8000/media/cafes/gallery1.jpg"],
            "opening_hours": {
                "monday": "08:00-22:00",
                "tuesday": "08:00-22:00"
            },
            "is_verified": true,
            "is_active": true,
            "created_at": "2024-01-01T10:00:00Z"
        }
    ]
}
```

### 2. ایجاد کافه جدید

**Endpoint:** `POST /api/cafes/`

**نیاز به احراز هویت**

**Request Body:**
```json
{
    "name": "کافه جدید",
    "description": "کافه جدید و مدرن",
    "cafe_type": "modern",
    "phone_number": "02187654321",
    "address": "تهران، خیابان کریمخان",
    "city": "تهران",
    "latitude": "35.7000",
    "longitude": "51.4000",
    "capacity": 30,
    "has_wifi": true,
    "has_parking": false,
    "is_smoking_allowed": false,
    "has_outdoor_seating": true,
    "opening_hours": {
        "monday": "09:00-23:00",
        "tuesday": "09:00-23:00"
    }
}
```

**Response (201 Created):**
```json
{
    "id": 2,
    "name": "کافه جدید",
    "description": "کافه جدید و مدرن",
    "cafe_type": "modern",
    "phone_number": "02187654321",
    "address": "تهران، خیابان کریمخان",
    "city": "تهران",
    "latitude": "35.7000",
    "longitude": "51.4000",
    "capacity": 30,
    "has_wifi": true,
    "has_parking": false,
    "is_smoking_allowed": false,
    "has_outdoor_seating": true,
    "average_rating": 0.0,
    "total_reviews": 0,
    "main_image": null,
    "gallery": [],
    "opening_hours": {
        "monday": "09:00-23:00",
        "tuesday": "09:00-23:00"
    },
    "is_verified": false,
    "is_active": true,
    "is_approved": false,
    "created_at": "2024-01-01T10:00:00Z"
}
```

### 3. مشاهده جزئیات کافه

**Endpoint:** `GET /api/cafes/{id}/`

**بدون احراز هویت**

**Response (200 OK):**
```json
{
    "id": 1,
    "name": "کافه مرکزی",
    "description": "کافه دنج در مرکز شهر",
    "cafe_type": "modern",
    "phone_number": "02112345678",
    "address": "تهران، خیابان ولیعصر",
    "city": "تهران",
    "latitude": "35.6892",
    "longitude": "51.3890",
    "capacity": 50,
    "has_wifi": true,
    "has_parking": true,
    "is_smoking_allowed": false,
    "has_outdoor_seating": true,
    "average_rating": 4.5,
    "total_reviews": 120,
    "main_image": "http://localhost:8000/media/cafes/cafe1.jpg",
    "gallery": ["http://localhost:8000/media/cafes/gallery1.jpg"],
    "opening_hours": {
        "monday": "08:00-22:00",
        "tuesday": "08:00-22:00"
    },
    "is_verified": true,
    "is_active": true,
    "created_at": "2024-01-01T10:00:00Z",
    "owner": {
        "id": 1,
        "first_name": "علی",
        "last_name": "احمدی",
        "phone_number": "09123456789"
    }
}
```

### 4. ویرایش کافه

**Endpoint:** `PUT /api/cafes/{id}/`

**نیاز به احراز هویت (فقط مالک یا ادمین)**

**Request Body:**
```json
{
    "name": "کافه مرکزی ویرایش شده",
    "description": "کافه دنج و مدرن در مرکز شهر",
    "capacity": 60,
    "has_wifi": true,
    "has_parking": true
}
```

### 5. حذف کافه

**Endpoint:** `DELETE /api/cafes/{id}/`

**نیاز به احراز هویت (فقط مالک یا ادمین)**

**Response (204 No Content)**

### 6. کافه‌های کاربر

**Endpoint:** `GET /api/cafes/my/`

**نیاز به احراز هویت**

**Response (200 OK):**
```json
{
    "count": 2,
    "results": [
        {
            "id": 1,
            "name": "کافه مرکزی",
            "city": "تهران",
            "is_approved": true,
            "is_active": true,
            "created_at": "2024-01-01T10:00:00Z"
        }
    ],
    "stats": {
        "total": 2,
        "approved": 1,
        "pending": 1
    }
}
```

---

## 🍽️ API های منوی کافه

### 1. لیست منوی کافه

**Endpoint:** `GET /api/cafes/{cafe_id}/menu/`

**بدون احراز هویت**

**Response (200 OK):**
```json
[
    {
        "id": 1,
        "cafe": 1,
        "name": "قهوه اسپرسو",
        "description": "قهوه اسپرسو خوشمزه",
        "category": "drinks",
        "price": "15000.00",
        "image": "http://localhost:8000/media/menu/espresso.jpg",
        "is_available": true,
        "is_popular": true,
        "created_at": "2024-01-01T10:00:00Z"
    }
]
```

### 2. اضافه کردن آیتم منو

**Endpoint:** `POST /api/cafes/{cafe_id}/menu/`

**نیاز به احراز هویت (فقط مالک کافه یا ادمین)**

**Request Body:**
```json
{
    "name": "کاپوچینو",
    "description": "کاپوچینو خوشمزه",
    "category": "drinks",
    "price": "20000",
    "is_available": true,
    "is_popular": false
}
```

### 3. ویرایش آیتم منو

**Endpoint:** `PUT /api/cafes/{cafe_id}/menu/{id}/`

**نیاز به احراز هویت (فقط مالک کافه یا ادمین)**

### 4. حذف آیتم منو

**Endpoint:** `DELETE /api/cafes/{cafe_id}/menu/{id}/`

**نیاز به احراز هویت (فقط مالک کافه یا ادمین)**

---

## ❤️ API های لایک

### 1. لایک کردن کافه

**Endpoint:** `POST /api/cafes/{cafe_id}/likes/`

**نیاز به احراز هویت**

**Request Body:**
```json
{
    "cafe": 1
}
```

**Response (201 Created):**
```json
{
    "id": 1,
    "user": 1,
    "cafe": 1,
    "user_name": "علی",
    "cafe_name": "کافه مرکزی",
    "created_at": "2024-01-01T10:00:00Z"
}
```

### 2. حذف لایک

**Endpoint:** `DELETE /api/cafes/{cafe_id}/unlike/`

**نیاز به احراز هویت**

**Response (200 OK):**
```json
{
    "message": "لایک با موفقیت حذف شد"
}
```

---

## 💬 API های کامنت

### 1. کامنت کردن کافه

**Endpoint:** `POST /api/cafes/{cafe_id}/comments/`

**نیاز به احراز هویت**

**Request Body:**
```json
{
    "cafe": 1,
    "content": "کافه خوبی بود، قهوه‌هاش عالی بود",
    "rating": 4
}
```

**Response (201 Created):**
```json
{
    "id": 1,
    "user": 1,
    "cafe": 1,
    "content": "کافه خوبی بود، قهوه‌هاش عالی بود",
    "rating": 4,
    "is_verified": false,
    "user_name": "علی",
    "cafe_name": "کافه مرکزی",
    "created_at": "2024-01-01T10:00:00Z"
}
```

### 2. لیست کامنت‌های کافه

**Endpoint:** `GET /api/cafes/{cafe_id}/comments/`

**بدون احراز هویت (فقط کامنت‌های تایید شده)**

**Response (200 OK):**
```json
[
    {
        "id": 1,
        "user": 1,
        "cafe": 1,
        "content": "کافه خوبی بود، قهوه‌هاش عالی بود",
        "rating": 4,
        "is_verified": true,
        "user_name": "علی",
        "cafe_name": "کافه مرکزی",
        "created_at": "2024-01-01T10:00:00Z"
    }
]
```

### 3. ویرایش کامنت

**Endpoint:** `PUT /api/cafes/{cafe_id}/comments/{id}/`

**نیاز به احراز هویت (فقط نویسنده کامنت)**

### 4. حذف کامنت

**Endpoint:** `DELETE /api/cafes/{cafe_id}/comments/{id}/`

**نیاز به احراز هویت (فقط نویسنده کامنت)**

---

## 🔍 API های جستجو و پیشنهاد

### 1. جستجوی کافه‌ها

**Endpoint:** `POST /api/search/`

**بدون احراز هویت**

**Request Body:**
```json
{
    "query": "کافه مدرن",
    "city": "تهران",
    "cafe_type": "modern",
    "has_wifi": true,
    "has_parking": true,
    "min_rating": 4.0,
    "latitude": "35.6892",
    "longitude": "51.3890",
    "radius": 5,
    "limit": 10
}
```

**Response (200 OK):**
```json
{
    "count": 5,
    "results": [
        {
            "id": 1,
            "name": "کافه مرکزی",
            "description": "کافه دنج در مرکز شهر",
            "cafe_type": "modern",
            "city": "تهران",
            "latitude": "35.6892",
            "longitude": "51.3890",
            "average_rating": 4.5,
            "total_reviews": 120,
            "distance": 0.5
        }
    ]
}
```

### 2. پیشنهاد کافه‌ها

**Endpoint:** `POST /api/recommendations/`

**بدون احراز هویت**

**Request Body:**
```json
{
    "latitude": "35.6892",
    "longitude": "51.3890",
    "radius": 5,
    "limit": 10,
    "cafe_types": ["modern", "traditional"],
    "min_rating": 4.0
}
```

**Response (200 OK):**
```json
{
    "count": 8,
    "user_location": {
        "latitude": "35.6892",
        "longitude": "51.3890"
    },
    "results": [
        {
            "id": 1,
            "name": "کافه مرکزی",
            "description": "کافه دنج در مرکز شهر",
            "cafe_type": "modern",
            "city": "تهران",
            "latitude": "35.6892",
            "longitude": "51.3890",
            "average_rating": 4.5,
            "total_reviews": 120,
            "distance": 0.5,
            "recommendation_score": 0.95
        }
    ]
}
```

---

## 📊 کدهای وضعیت HTTP

| کد | معنی | توضیح |
|---|---|---|
| 200 | OK | درخواست موفق |
| 201 | Created | منبع جدید ایجاد شد |
| 204 | No Content | درخواست موفق، بدون محتوا |
| 400 | Bad Request | درخواست نامعتبر |
| 401 | Unauthorized | نیاز به احراز هویت |
| 403 | Forbidden | دسترسی غیرمجاز |
| 404 | Not Found | منبع یافت نشد |
| 500 | Internal Server Error | خطای سرور |

---

## ⚠️ خطاها

### نمونه پاسخ خطا:

```json
{
    "error": "خطا در پردازش درخواست",
    "details": {
        "field_name": ["این فیلد الزامی است"],
        "phone_number": ["شماره تلفن قبلاً ثبت شده است"]
    }
}
```

### خطاهای رایج:

- **400 Bad Request**: داده‌های ارسالی نامعتبر
- **401 Unauthorized**: نیاز به احراز هویت
- **403 Forbidden**: دسترسی غیرمجاز
- **404 Not Found**: منبع یافت نشد
- **500 Internal Server Error**: خطای سرور

---

## 🔧 تنظیمات محیط

### متغیرهای محیطی مورد نیاز:

```bash
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### نصب و راه‌اندازی:

```bash
# نصب dependencies
pip install -r requirements.txt

# اجرای migrations
python manage.py migrate

# ایجاد superuser
python manage.py createsuperuser

# اجرای سرور
python manage.py runserver
```

---

## 📝 نکات مهم

1. **احراز هویت**: برای دسترسی به API های محافظت شده، token را در header ارسال کنید
2. **Rate Limiting**: در حال حاضر محدودیت نرخ وجود ندارد
3. **Pagination**: لیست‌ها به صورت صفحه‌بندی شده برگردانده می‌شوند
4. **Validation**: تمام داده‌های ورودی اعتبارسنجی می‌شوند
5. **Permissions**: دسترسی‌ها بر اساس نقش کاربر کنترل می‌شوند

---

## 🚀 مثال‌های استفاده

### مثال کامل با cURL:

```bash
# ثبت‌نام
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "09123456789",
    "first_name": "علی",
    "last_name": "احمدی",
    "email": "ali@example.com",
    "password": "password123",
    "password_confirm": "password123"
  }'

# لاگین
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "09123456789",
    "password": "password123"
  }'

# دریافت لیست کافه‌ها
curl -X GET http://localhost:8000/api/cafes/ \
  -H "Authorization: Token abc123def456..."

# جستجوی کافه
curl -X POST http://localhost:8000/api/search/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "کافه مدرن",
    "city": "تهران",
    "has_wifi": true
  }'
```

---

## 📞 پشتیبانی

برای سوالات و پشتیبانی، با تیم توسعه تماس بگیرید.

**نسخه API:** 1.0  
**آخرین به‌روزرسانی:** 2024-01-01
