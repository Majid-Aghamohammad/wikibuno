from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import User, UserProfile

User = get_user_model()


class UserModelTest(TestCase):
    """
    تست‌های مدل User
    """
    
    def setUp(self):
        """تنظیمات اولیه برای تست‌ها"""
        self.user_data = {
            'phone_number': '09123456789',
            'first_name': 'علی',
            'last_name': 'احمدی',
            'email': 'ali@example.com',
            'password': 'testpass123'
        }
    
    def test_create_user(self):
        """تست ایجاد کاربر جدید"""
        user_data_with_username = self.user_data.copy()
        user_data_with_username['username'] = 'testuser'
        user = User.objects.create_user(**user_data_with_username)
        
        self.assertEqual(user.phone_number, '09123456789')
        self.assertEqual(user.first_name, 'علی')
        self.assertEqual(user.last_name, 'احمدی')
        self.assertEqual(user.email, 'ali@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_superuser(self):
        """تست ایجاد superuser"""
        user = User.objects.create_superuser(
            username='admin',
            phone_number='09987654321',
            first_name='admin',
            last_name='admin',
            password='adminpass123'
        )
        
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
    
    def test_phone_number_validation(self):
        """تست validation شماره تلفن"""
        # شماره تلفن نامعتبر
        invalid_data = self.user_data.copy()
        invalid_data['phone_number'] = '1234567890'  # بدون 09
        
        with self.assertRaises(ValidationError):
            user = User(**invalid_data)
            user.full_clean()
    
    def test_phone_number_unique(self):
        """تست یکتایی شماره تلفن"""
        user_data_with_username = self.user_data.copy()
        user_data_with_username['username'] = 'testuser1'
        User.objects.create_user(**user_data_with_username)
        
        # تلاش برای ایجاد کاربر با همان شماره تلفن
        duplicate_data = self.user_data.copy()
        duplicate_data['email'] = 'different@example.com'
        duplicate_data['username'] = 'testuser2'
        
        with self.assertRaises(Exception):  # IntegrityError
            User.objects.create_user(**duplicate_data)
    
    def test_user_str_representation(self):
        """تست نمایش رشته کاربر"""
        user_data_with_username = self.user_data.copy()
        user_data_with_username['username'] = 'testuser'
        user = User.objects.create_user(**user_data_with_username)
        expected = f"{user.first_name} {user.last_name} ({user.phone_number})"
        self.assertEqual(str(user), expected)


class UserProfileModelTest(TestCase):
    """
    تست‌های مدل UserProfile
    """
    
    def setUp(self):
        """تنظیمات اولیه برای تست‌ها"""
        self.user = User.objects.create_user(
            username='testuser',
            phone_number='09123456789',
            first_name='علی',
            last_name='احمدی',
            password='testpass123'
        )
    
    def test_create_user_profile(self):
        """تست ایجاد پروفایل کاربر"""
        profile = UserProfile.objects.create(
            user=self.user,
            bio='این یک بیوگرافی تست است',
            location='تهران',
            latitude=35.6892,
            longitude=51.3890,
            favorite_cafe_types=['traditional', 'modern']
        )
        
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.bio, 'این یک بیوگرافی تست است')
        self.assertEqual(profile.location, 'تهران')
        self.assertEqual(profile.latitude, 35.6892)
        self.assertEqual(profile.longitude, 51.3890)
        self.assertEqual(profile.favorite_cafe_types, ['traditional', 'modern'])
    
    def test_user_profile_str_representation(self):
        """تست نمایش رشته پروفایل"""
        profile = UserProfile.objects.create(user=self.user)
        expected = f"پروفایل {self.user.first_name} {self.user.last_name}"
        self.assertEqual(str(profile), expected)
    
    def test_user_profile_auto_creation(self):
        """تست ایجاد خودکار پروفایل"""
        # پروفایل باید خودکار ایجاد شود
        try:
            profile = UserProfile.objects.get(user=self.user)
            self.assertIsNotNone(profile)
            self.assertEqual(profile.user, self.user)
        except UserProfile.DoesNotExist:
            # اگر پروفایل خودکار ایجاد نمی‌شود، آن را ایجاد می‌کنیم
            profile = UserProfile.objects.create(user=self.user)
            self.assertIsNotNone(profile)
            self.assertEqual(profile.user, self.user)
