# 🚀 راهنمای شروع سریع - WikiBuno

## ⚡ نصب و راه‌اندازی سریع

### 1. نصب Dependencies
```bash
pip install -r requirements.txt
```

### 2. اجرای Migration ها
```bash
python manage.py migrate
```

### 3. ایجاد Superuser
```bash
python manage.py createsuperuser
```

### 4. اجرای سرور
```bash
python manage.py runserver
```

### 5. دسترسی به Admin Panel
```
http://localhost:8000/admin/
```

---

## 🧪 تست کردن API

### 1. اجرای تست‌ها
```bash
# تمام تست‌ها
python manage.py test

# تست‌های خاص
python manage.py test user.tests
python manage.py test buno.tests
```

### 2. استفاده از Postman
1. فایل `WikiBuno_API.postman_collection.json` را در Postman import کنید
2. فایل `WikiBuno_Environment.postman_environment.json` را import کنید
3. Environment را انتخاب کنید
4. API ها را تست کنید

---

## 📱 مثال‌های استفاده

### ثبت‌نام کاربر
```bash
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
```

### لاگین
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "09123456789",
    "password": "password123"
  }'
```

### دریافت لیست کافه‌ها
```bash
curl -X GET http://localhost:8000/api/cafes/
```

### جستجوی کافه
```bash
curl -X POST http://localhost:8000/api/search/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "کافه مدرن",
    "city": "تهران",
    "has_wifi": true
  }'
```

---

## 🔑 نکات مهم

1. **Token Authentication**: برای API های محافظت شده، token را در header ارسال کنید
2. **Base URL**: `http://localhost:8000/api/`
3. **Admin Panel**: `http://localhost:8000/admin/`
4. **مستندات کامل**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

---

## 📊 آمار پروژه

- **48 تست واحد** ✅
- **27 API endpoint** ✅
- **6 مدل اصلی** ✅
- **Django Admin** ✅
- **Token Authentication** ✅
- **Search & Recommendations** ✅

---

## 🆘 حل مشکلات

### مشکل: Migration ها اجرا نمی‌شوند
```bash
python manage.py makemigrations
python manage.py migrate
```

### مشکل: Superuser ایجاد نمی‌شود
```bash
python manage.py createsuperuser
# یا از فایل create_superuser.py استفاده کنید
python create_superuser.py
```

### مشکل: تست‌ها fail می‌شوند
```bash
# بررسی dependencies
pip install -r requirements.txt

# اجرای تست‌ها با verbose
python manage.py test -v 2
```

---

## 📞 پشتیبانی

برای سوالات و مشکلات:
- مستندات کامل: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- README اصلی: [README.md](README.md)
- Postman Collection: [WikiBuno_API.postman_collection.json](WikiBuno_API.postman_collection.json)

**آماده برای استفاده! 🎉**
