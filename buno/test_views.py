from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from decimal import Decimal
from .models import Cafe, CafeMenu, Like, Comment

User = get_user_model()


class CafeAPITest(APITestCase):
    """
    تست‌های API کافه‌ها
    """
    
    def setUp(self):
        """تنظیمات اولیه برای تست‌ها"""
        self.cafe_list_url = reverse('buno:cafe_list')
        self.cafe_detail_url = lambda id: reverse('buno:cafe_detail', kwargs={'pk': id})
        self.cafe_menu_url = lambda id: reverse('buno:cafe_menu', kwargs={'cafe_id': id})
        self.like_url = lambda id: reverse('buno:cafe_likes', kwargs={'cafe_id': id})
        self.unlike_url = lambda id: reverse('buno:unlike_cafe', kwargs={'cafe_id': id})
        self.comment_url = lambda id: reverse('buno:cafe_comments', kwargs={'cafe_id': id})
        self.search_url = reverse('buno:search_cafes')
        self.recommend_url = reverse('buno:recommend_cafes')
        self.user_cafes_url = reverse('buno:user_cafes')
        
        # ایجاد کاربر
        self.user = User.objects.create_user(
            username='testuser',
            phone_number='09123456789',
            first_name='علی',
            last_name='احمدی',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        
        # ایجاد کافه
        self.cafe = Cafe.objects.create(
            name='کافه تست',
            description='کافه تست برای تست',
            cafe_type='modern',
            phone_number='02112345678',
            address='تهران، خیابان ولیعصر',
            city='تهران',
            latitude=Decimal('35.6892'),
            longitude=Decimal('51.3890'),
            capacity=50,
            owner=self.user,
            is_approved=True  # تایید شده برای تست
        )
    
    def test_cafe_list_public_access(self):
        """تست دسترسی عمومی به لیست کافه‌ها"""
        response = self.client.get(self.cafe_list_url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
        self.assertEqual(response.data['count'], 1)
    
    def test_cafe_create_authenticated(self):
        """تست ایجاد کافه توسط کاربر احراز هویت شده"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        cafe_data = {
            'name': 'کافه جدید',
            'description': 'کافه جدید برای تست',
            'cafe_type': 'traditional',
            'phone_number': '02187654321',
            'address': 'تهران، خیابان کریمخان',
            'city': 'تهران',
            'latitude': '35.7000',
            'longitude': '51.4000',
            'capacity': 30
        }
        
        response = self.client.post(self.cafe_list_url, cafe_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'کافه جدید')
        self.assertFalse(response.data['is_approved'])  # نیاز به تایید ادمین
    
    def test_cafe_create_unauthorized(self):
        """تست ایجاد کافه بدون احراز هویت"""
        cafe_data = {
            'name': 'کافه جدید',
            'description': 'کافه جدید برای تست',
            'cafe_type': 'traditional'
        }
        
        response = self.client.post(self.cafe_list_url, cafe_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_cafe_detail_public_access(self):
        """تست دسترسی عمومی به جزئیات کافه"""
        response = self.client.get(self.cafe_detail_url(self.cafe.id), format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'کافه تست')
        self.assertEqual(response.data['city'], 'تهران')
    
    def test_cafe_update_owner(self):
        """تست ویرایش کافه توسط مالک"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        update_data = {
            'name': 'کافه تست ویرایش شده',
            'description': 'توضیحات ویرایش شده',
            'capacity': 60
        }
        
        response = self.client.put(self.cafe_detail_url(self.cafe.id), update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'کافه تست ویرایش شده')
        self.assertEqual(response.data['capacity'], 60)
        self.assertFalse(response.data['is_approved'])  # پس از ویرایش نیاز به تایید مجدد
    
    def test_cafe_update_non_owner(self):
        """تست ویرایش کافه توسط غیرمالک"""
        # ایجاد کاربر دیگر
        other_user = User.objects.create_user(
            username='otheruser',
            phone_number='09987654321',
            first_name='فاطمه',
            last_name='محمدی',
            password='testpass123'
        )
        other_token = Token.objects.create(user=other_user)
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {other_token.key}')
        
        update_data = {
            'name': 'کافه تست ویرایش شده',
            'description': 'توضیحات ویرایش شده'
        }
        
        response = self.client.put(self.cafe_detail_url(self.cafe.id), update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_cafe_delete_owner(self):
        """تست حذف کافه توسط مالک"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        response = self.client.delete(self.cafe_detail_url(self.cafe.id), format='json')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Cafe.objects.filter(id=self.cafe.id).exists())
    
    def test_cafe_menu_list(self):
        """تست لیست منوی کافه"""
        # ایجاد آیتم منو
        CafeMenu.objects.create(
            cafe=self.cafe,
            name='قهوه اسپرسو',
            description='قهوه اسپرسو خوشمزه',
            category='drinks',
            price=Decimal('15000')
        )
        
        response = self.client.get(self.cafe_menu_url(self.cafe.id), format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # بررسی وجود آیتم مورد نظر
        if isinstance(response.data, list):
            menu_names = [item['name'] for item in response.data]
            self.assertIn('قهوه اسپرسو', menu_names)
        else:
            # اگر response.data یک dict است
            self.assertIn('results', response.data)
            menu_names = [item['name'] for item in response.data['results']]
            self.assertIn('قهوه اسپرسو', menu_names)
    
    def test_cafe_menu_create(self):
        """تست ایجاد آیتم منو"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        menu_data = {
            'name': 'کاپوچینو',
            'description': 'کاپوچینو خوشمزه',
            'category': 'drinks',
            'price': '20000'
        }
        
        response = self.client.post(self.cafe_menu_url(self.cafe.id), menu_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'کاپوچینو')
        self.assertEqual(response.data['cafe'], self.cafe.id)
    
    def test_like_cafe(self):
        """تست لایک کردن کافه"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        like_data = {'cafe': self.cafe.id}
        response = self.client.post(self.like_url(self.cafe.id), like_data, format='json')
        
        if response.status_code != status.HTTP_201_CREATED:
            print(f"Response data: {response.data}")
            print(f"Response status: {response.status_code}")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Like.objects.filter(user=self.user, cafe=self.cafe).exists())
    
    def test_unlike_cafe(self):
        """تست حذف لایک کافه"""
        # ایجاد لایک
        Like.objects.create(user=self.user, cafe=self.cafe)
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        response = self.client.delete(self.unlike_url(self.cafe.id), format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Like.objects.filter(user=self.user, cafe=self.cafe).exists())
    
    def test_comment_cafe(self):
        """تست کامنت کردن کافه"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        comment_data = {
            'cafe': self.cafe.id,
            'content': 'کافه خوبی بود',
            'rating': 4
        }
        
        response = self.client.post(self.comment_url(self.cafe.id), comment_data, format='json')
        
        if response.status_code != status.HTTP_201_CREATED:
            print(f"Response data: {response.data}")
            print(f"Response status: {response.status_code}")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], 'کافه خوبی بود')
        self.assertEqual(response.data['rating'], 4)
        self.assertTrue(Comment.objects.filter(user=self.user, cafe=self.cafe).exists())
    
    def test_comment_list(self):
        """تست لیست کامنت‌های کافه"""
        # ایجاد کامنت
        Comment.objects.create(
            user=self.user,
            cafe=self.cafe,
            content='کافه خوبی بود',
            rating=4,
            is_verified=True
        )
        
        response = self.client.get(self.comment_url(self.cafe.id), format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # بررسی وجود کامنت مورد نظر
        if isinstance(response.data, list):
            comment_contents = [item['content'] for item in response.data]
            self.assertIn('کافه خوبی بود', comment_contents)
        else:
            # اگر response.data یک dict است
            self.assertIn('results', response.data)
            comment_contents = [item['content'] for item in response.data['results']]
            self.assertIn('کافه خوبی بود', comment_contents)
    
    def test_search_cafes(self):
        """تست جستجوی کافه‌ها"""
        search_data = {
            'query': 'تست',
            'city': 'تهران',
            'cafe_type': 'modern'
        }
        
        response = self.client.post(self.search_url, search_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
        self.assertEqual(response.data['count'], 1)
    
    def test_recommend_cafes(self):
        """تست پیشنهاد کافه‌ها"""
        recommend_data = {
            'latitude': '35.6892',
            'longitude': '51.3890',
            'radius': 5,
            'limit': 10
        }
        
        response = self.client.post(self.recommend_url, recommend_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
        self.assertIn('user_location', response.data)
        self.assertEqual(response.data['count'], 1)
    
    def test_user_cafes(self):
        """تست کافه‌های کاربر"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        response = self.client.get(self.user_cafes_url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
        self.assertIn('stats', response.data)
        self.assertEqual(response.data['count'], 1)
        
        # بررسی آمار
        stats = response.data['stats']
        self.assertEqual(stats['total'], 1)
        self.assertEqual(stats['approved'], 1)
        self.assertEqual(stats['pending'], 0)
    
    def test_unauthorized_access(self):
        """تست دسترسی غیرمجاز"""
        # درخواست بدون token
        response = self.client.post(self.cafe_list_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        response = self.client.post(self.like_url(self.cafe.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        response = self.client.post(self.comment_url(self.cafe.id), {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        response = self.client.get(self.user_cafes_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
