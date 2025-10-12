from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class User(AbstractUser):
    """
    مدل کاربر سفارشی برای سیستم پیشنهاد کافه
    """
    phone_regex = RegexValidator(
        regex=r'^09\d{9}$',
        message="شماره تلفن باید با 09 شروع شود و 11 رقم باشد"
    )
    
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=11,
        unique=True,
        verbose_name="شماره تلفن"
    )
    
    first_name = models.CharField(max_length=30, verbose_name="نام")
    last_name = models.CharField(max_length=30, verbose_name="نام خانوادگی")
    
    # حذف فیلدهای غیرضروری از AbstractUser
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(blank=True, null=True, verbose_name="ایمیل")
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone_number})"


class UserProfile(models.Model):
    """
    پروفایل کاربر شامل اطلاعات تکمیلی
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile',
        verbose_name="کاربر"
    )
    
    bio = models.TextField(
        max_length=500, 
        blank=True, 
        verbose_name="درباره من"
    )
    
    avatar = models.ImageField(
        upload_to='avatars/', 
        blank=True, 
        null=True,
        verbose_name="عکس پروفایل"
    )
    
    birth_date = models.DateField(
        blank=True, 
        null=True,
        verbose_name="تاریخ تولد"
    )
    
    location = models.CharField(
        max_length=100, 
        blank=True,
        verbose_name="موقعیت مکانی"
    )
    
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        blank=True, 
        null=True,
        verbose_name="عرض جغرافیایی"
    )
    
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        blank=True, 
        null=True,
        verbose_name="طول جغرافیایی"
    )
    
    favorite_cafe_types = models.JSONField(
        default=list,
        blank=True,
        verbose_name="انواع کافه مورد علاقه"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")
    
    class Meta:
        verbose_name = "پروفایل کاربر"
        verbose_name_plural = "پروفایل‌های کاربران"
    
    def __str__(self):
        return f"پروفایل {self.user.first_name} {self.user.last_name}"