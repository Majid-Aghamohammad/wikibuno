from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

User = get_user_model()

# Create your models here.

class Cafe(models.Model):
    """
    مدل کافه شامل اطلاعات کامل کافه
    """
    CAFE_TYPES = [
        ('traditional', 'سنتی'),
        ('modern', 'مدرن'),
        ('cozy', 'دنج'),
        ('luxury', 'لوکس'),
        ('budget', 'اقتصادی'),
        ('rooftop', 'پشت‌بام'),
        ('garden', 'باغی'),
        ('library', 'کتابخانه‌ای'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="نام کافه")
    description = models.TextField(verbose_name="توضیحات")
    cafe_type = models.CharField(
        max_length=20, 
        choices=CAFE_TYPES, 
        default='modern',
        verbose_name="نوع کافه"
    )
    
    # اطلاعات تماس
    phone_number = models.CharField(max_length=11, default='09123456789', verbose_name="شماره تلفن")
    address = models.TextField(default='آدرس وارد نشده', verbose_name="آدرس")
    city = models.CharField(max_length=50, default='تهران', verbose_name="شهر")
    
    # موقعیت جغرافیایی
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        default=35.6892,
        verbose_name="عرض جغرافیایی"
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        default=51.3890,
        verbose_name="طول جغرافیایی"
    )
    
    # اطلاعات کافه
    capacity = models.PositiveIntegerField(default=50, verbose_name="ظرفیت")
    has_wifi = models.BooleanField(default=True, verbose_name="وای‌فای")
    has_parking = models.BooleanField(default=False, verbose_name="پارکینگ")
    is_smoking_allowed = models.BooleanField(default=False, verbose_name="سیگار مجاز")
    has_outdoor_seating = models.BooleanField(default=False, verbose_name="محوطه باز")
    
    # امتیاز و رتبه‌بندی
    average_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="میانگین امتیاز"
    )
    total_reviews = models.PositiveIntegerField(default=0, verbose_name="تعداد نظرات")
    
    # تصاویر
    main_image = models.ImageField(
        upload_to='cafes/main/', 
        blank=True,
        null=True,
        verbose_name="تصویر اصلی"
    )
    gallery = models.JSONField(
        default=list, 
        blank=True,
        verbose_name="گالری تصاویر"
    )
    
    # مالکیت
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='owned_cafes',
        verbose_name="مالک"
    )
    
    # وضعیت
    is_verified = models.BooleanField(default=False, verbose_name="تایید شده")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    is_approved = models.BooleanField(default=False, verbose_name="تایید ادمین")
    approval_date = models.DateTimeField(blank=True, null=True, verbose_name="تاریخ تایید")
    approved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        related_name='approved_cafes',
        verbose_name="تایید کننده"
    )
    
    # زمان‌ها
    opening_hours = models.JSONField(
        default=dict,
        verbose_name="ساعات کاری"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")
    
    class Meta:
        verbose_name = "کافه"
        verbose_name_plural = "کافه‌ها"
        ordering = ['-average_rating', '-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.city}"
    
    def update_rating(self):
        """به‌روزرسانی امتیاز میانگین کافه"""
        from django.db.models import Avg
        avg_rating = self.comments.aggregate(avg=Avg('rating'))['avg']
        if avg_rating:
            self.average_rating = round(avg_rating, 2)
        else:
            self.average_rating = 0.00
        self.total_reviews = self.comments.count()
        self.save(update_fields=['average_rating', 'total_reviews'])


class CafeMenu(models.Model):
    """
    مدل منوی کافه
    """
    CATEGORIES = [
        ('drinks', 'نوشیدنی'),
        ('food', 'غذا'),
        ('dessert', 'دسر'),
        ('snack', 'تنقلات'),
        ('breakfast', 'صبحانه'),
    ]
    
    cafe = models.ForeignKey(
        Cafe, 
        on_delete=models.CASCADE, 
        related_name='menu_items',
        verbose_name="کافه"
    )
    
    name = models.CharField(max_length=100, verbose_name="نام آیتم")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    category = models.CharField(
        max_length=20, 
        choices=CATEGORIES, 
        verbose_name="دسته‌بندی"
    )
    
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=0, 
        verbose_name="قیمت (تومان)"
    )
    
    image = models.ImageField(
        upload_to='cafes/menu/', 
        blank=True, 
        null=True,
        verbose_name="تصویر"
    )
    
    is_available = models.BooleanField(default=True, verbose_name="موجود")
    is_popular = models.BooleanField(default=False, verbose_name="محبوب")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")
    
    class Meta:
        verbose_name = "آیتم منو"
        verbose_name_plural = "آیتم‌های منو"
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.cafe.name}"


class Like(models.Model):
    """
    مدل لایک کافه‌ها
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='cafe_likes',
        verbose_name="کاربر"
    )
    
    cafe = models.ForeignKey(
        Cafe, 
        on_delete=models.CASCADE, 
        related_name='likes',
        verbose_name="کافه"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    
    class Meta:
        verbose_name = "لایک"
        verbose_name_plural = "لایک‌ها"
        unique_together = ['user', 'cafe']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.first_name} لایک کرد {self.cafe.name}"


class Comment(models.Model):
    """
    مدل کامنت کافه‌ها
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='cafe_comments',
        verbose_name="کاربر"
    )
    
    cafe = models.ForeignKey(
        Cafe, 
        on_delete=models.CASCADE, 
        related_name='comments',
        verbose_name="کافه"
    )
    
    content = models.TextField(verbose_name="متن کامنت")
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="امتیاز"
    )
    
    is_verified = models.BooleanField(default=False, verbose_name="تایید شده")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")
    
    class Meta:
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت‌ها"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"کامنت {self.user.first_name} برای {self.cafe.name}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # به‌روزرسانی امتیاز کافه پس از ذخیره کامنت
        self.cafe.update_rating()

