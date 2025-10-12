from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from decimal import Decimal
from .models import UserProfile

User = get_user_model()


class UserAuthenticationAPITest(APITestCase):
    """
    تست‌های API احراز هویت کاربران
    """
    
    def setUp(self):
        """تنظیمات اولیه برای تست‌ها"""
        self.register_url = reverse('user:register')
        self.login_url = reverse('user:login')
        self.logout_url = reverse('user:logout')
        self.profile_url = reverse('user:profile')
        self.dashboard_url = reverse('user:dashboard')
        
        self.user_data = {
            'phone_number': '09123456789',
            'first_name': 'علی',
            'last_name': 'احمدی',
            'email': 'ali@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123'
        }
    
    def test_user_registration(self):
        """تست ثبت‌نام کاربر جدید"""
        response = self.client.post(self.register_url, self.user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertIn('user', response.data)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user']['phone_number'], '09123456789')
        
        # بررسی ایجاد کاربر در دیتابیس
        self.assertTrue(User.objects.filter(phone_number='09123456789').exists())
        
        # بررسی ایجاد پروفایل خودکار
        user = User.objects.get(phone_number='09123456789')
        self.assertTrue(UserProfile.objects.filter(user=user).exists())
    
    def test_user_registration_duplicate_phone(self):
        """تست ثبت‌نام با شماره تلفن تکراری"""
        # ایجاد کاربر اول
        User.objects.create_user(
            username='user1',
            phone_number='09123456789',
            first_name='کاربر',
            last_name='اول',
            password='testpass123'
        )
        
        # تلاش برای ثبت‌نام با همان شماره تلفن
        response = self.client.post(self.register_url, self.user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone_number', response.data)
    
    def test_user_registration_password_mismatch(self):
        """تست ثبت‌نام با رمزهای عبور متفاوت"""
        invalid_data = self.user_data.copy()
        invalid_data['password_confirm'] = 'differentpass'
        
        response = self.client.post(self.register_url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
    
    def test_user_login(self):
        """تست لاگین کاربر"""
        # ایجاد کاربر
        user = User.objects.create_user(
            username='testuser',
            phone_number='09123456789',
            first_name='علی',
            last_name='احمدی',
            password='testpass123'
        )
        
        login_data = {
            'phone_number': '09123456789',
            'password': 'testpass123'
        }
        
        response = self.client.post(self.login_url, login_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('user', response.data)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user']['phone_number'], '09123456789')
    
    def test_user_login_invalid_credentials(self):
        """تست لاگین با اطلاعات نادرست"""
        login_data = {
            'phone_number': '09123456789',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(self.login_url, login_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
    
    def test_user_logout(self):
        """تست خروج کاربر"""
        # ایجاد و لاگین کاربر
        user = User.objects.create_user(
            username='testuser',
            phone_number='09123456789',
            first_name='علی',
            last_name='احمدی',
            password='testpass123'
        )
        token = Token.objects.create(user=user)
        
        # تنظیم token برای درخواست
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        response = self.client.post(self.logout_url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        
        # بررسی حذف token
        self.assertFalse(Token.objects.filter(user=user).exists())
    
    def test_user_profile_access(self):
        """تست دسترسی به پروفایل کاربر"""
        # ایجاد و لاگین کاربر
        user = User.objects.create_user(
            username='testuser',
            phone_number='09123456789',
            first_name='علی',
            last_name='احمدی',
            password='testpass123'
        )
        token = Token.objects.create(user=user)
        
        # تنظیم token برای درخواست
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        response = self.client.get(self.profile_url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone_number'], '09123456789')
        self.assertEqual(response.data['first_name'], 'علی')
        self.assertEqual(response.data['last_name'], 'احمدی')
    
    def test_user_profile_update(self):
        """تست به‌روزرسانی پروفایل کاربر"""
        # ایجاد و لاگین کاربر
        user = User.objects.create_user(
            username='testuser',
            phone_number='09123456789',
            first_name='علی',
            last_name='احمدی',
            password='testpass123'
        )
        token = Token.objects.create(user=user)
        
        # تنظیم token برای درخواست
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        update_data = {
            'first_name': 'علی‌رضا',
            'last_name': 'احمدی‌زاده',
            'email': 'alireza@example.com'
        }
        
        response = self.client.put(self.profile_url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'علی‌رضا')
        self.assertEqual(response.data['last_name'], 'احمدی‌زاده')
        self.assertEqual(response.data['email'], 'alireza@example.com')
    
    def test_user_dashboard(self):
        """تست داشبورد کاربر"""
        # ایجاد و لاگین کاربر
        user = User.objects.create_user(
            username='testuser',
            phone_number='09123456789',
            first_name='علی',
            last_name='احمدی',
            password='testpass123'
        )
        token = Token.objects.create(user=user)
        
        # تنظیم token برای درخواست
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        response = self.client.get(self.dashboard_url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertIn('profile', response.data)
        self.assertIn('stats', response.data)
        
        # بررسی آمار
        stats = response.data['stats']
        self.assertIn('owned_cafes', stats)
        self.assertIn('cafe_likes', stats)
        self.assertIn('cafe_comments', stats)
    
    def test_unauthorized_access(self):
        """تست دسترسی غیرمجاز"""
        # درخواست بدون token
        response = self.client.get(self.profile_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        response = self.client.get(self.dashboard_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        response = self.client.post(self.logout_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
