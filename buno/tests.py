from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal
from .models import Cafe, CafeMenu, Like, Comment

User = get_user_model()


class CafeModelTest(TestCase):
    """
    تست‌های مدل Cafe
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
        
        self.cafe_data = {
            'name': 'کافه تست',
            'description': 'این یک کافه تست است',
            'cafe_type': 'modern',
            'phone_number': '02112345678',
            'address': 'تهران، خیابان ولیعصر',
            'city': 'تهران',
            'latitude': Decimal('35.6892'),
            'longitude': Decimal('51.3890'),
            'capacity': 50,
            'owner': self.user
        }
    
    def test_create_cafe(self):
        """تست ایجاد کافه جدید"""
        cafe = Cafe.objects.create(**self.cafe_data)
        
        self.assertEqual(cafe.name, 'کافه تست')
        self.assertEqual(cafe.description, 'این یک کافه تست است')
        self.assertEqual(cafe.cafe_type, 'modern')
        self.assertEqual(cafe.owner, self.user)
        self.assertEqual(cafe.average_rating, Decimal('0.00'))
        self.assertEqual(cafe.total_reviews, 0)
        self.assertFalse(cafe.is_approved)
        self.assertTrue(cafe.is_active)
    
    def test_cafe_str_representation(self):
        """تست نمایش رشته کافه"""
        cafe = Cafe.objects.create(**self.cafe_data)
        expected = f"{cafe.name} - {cafe.city}"
        self.assertEqual(str(cafe), expected)
    
    def test_cafe_rating_update(self):
        """تست به‌روزرسانی امتیاز کافه"""
        cafe = Cafe.objects.create(**self.cafe_data)
        
        # ایجاد کامنت‌های تست
        user2 = User.objects.create_user(
            username='testuser2',
            phone_number='09987654321',
            first_name='فاطمه',
            last_name='محمدی',
            password='testpass123'
        )
        
        Comment.objects.create(
            user=user2,
            cafe=cafe,
            content='کافه خوبی بود',
            rating=4
        )
        
        Comment.objects.create(
            user=self.user,
            cafe=cafe,
            content='عالی بود',
            rating=5
        )
        
        # به‌روزرسانی امتیاز
        cafe.update_rating()
        
        self.assertEqual(cafe.average_rating, Decimal('4.50'))
        self.assertEqual(cafe.total_reviews, 2)
    
    def test_cafe_approval(self):
        """تست تایید کافه"""
        cafe = Cafe.objects.create(**self.cafe_data)
        
        # تایید کافه
        cafe.is_approved = True
        cafe.approved_by = self.user
        cafe.approval_date = timezone.now()
        cafe.save()
        
        self.assertTrue(cafe.is_approved)
        self.assertEqual(cafe.approved_by, self.user)
        self.assertIsNotNone(cafe.approval_date)


class CafeMenuModelTest(TestCase):
    """
    تست‌های مدل CafeMenu
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
        
        self.cafe = Cafe.objects.create(
            name='کافه تست',
            description='کافه تست',
            cafe_type='modern',
            phone_number='02112345678',
            address='تهران',
            city='تهران',
            latitude=Decimal('35.6892'),
            longitude=Decimal('51.3890'),
            capacity=50,
            owner=self.user
        )
    
    def test_create_menu_item(self):
        """تست ایجاد آیتم منو"""
        menu_item = CafeMenu.objects.create(
            cafe=self.cafe,
            name='قهوه اسپرسو',
            description='قهوه اسپرسو خوشمزه',
            category='drinks',
            price=Decimal('15000')
        )
        
        self.assertEqual(menu_item.cafe, self.cafe)
        self.assertEqual(menu_item.name, 'قهوه اسپرسو')
        self.assertEqual(menu_item.category, 'drinks')
        self.assertEqual(menu_item.price, Decimal('15000'))
        self.assertTrue(menu_item.is_available)
        self.assertFalse(menu_item.is_popular)
    
    def test_menu_item_str_representation(self):
        """تست نمایش رشته آیتم منو"""
        menu_item = CafeMenu.objects.create(
            cafe=self.cafe,
            name='قهوه اسپرسو',
            category='drinks',
            price=Decimal('15000')
        )
        expected = f"{menu_item.name} - {self.cafe.name}"
        self.assertEqual(str(menu_item), expected)


class LikeModelTest(TestCase):
    """
    تست‌های مدل Like
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
        
        self.cafe = Cafe.objects.create(
            name='کافه تست',
            description='کافه تست',
            cafe_type='modern',
            phone_number='02112345678',
            address='تهران',
            city='تهران',
            latitude=Decimal('35.6892'),
            longitude=Decimal('51.3890'),
            capacity=50,
            owner=self.user
        )
    
    def test_create_like(self):
        """تست ایجاد لایک"""
        like = Like.objects.create(
            user=self.user,
            cafe=self.cafe
        )
        
        self.assertEqual(like.user, self.user)
        self.assertEqual(like.cafe, self.cafe)
        self.assertIsNotNone(like.created_at)
    
    def test_like_str_representation(self):
        """تست نمایش رشته لایک"""
        like = Like.objects.create(
            user=self.user,
            cafe=self.cafe
        )
        expected = f"{self.user.first_name} لایک کرد {self.cafe.name}"
        self.assertEqual(str(like), expected)
    
    def test_unique_like_per_user_cafe(self):
        """تست یکتایی لایک برای هر کاربر-کافه"""
        Like.objects.create(user=self.user, cafe=self.cafe)
        
        # تلاش برای ایجاد لایک تکراری
        with self.assertRaises(Exception):  # IntegrityError
            Like.objects.create(user=self.user, cafe=self.cafe)


class CommentModelTest(TestCase):
    """
    تست‌های مدل Comment
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
        
        self.cafe = Cafe.objects.create(
            name='کافه تست',
            description='کافه تست',
            cafe_type='modern',
            phone_number='02112345678',
            address='تهران',
            city='تهران',
            latitude=Decimal('35.6892'),
            longitude=Decimal('51.3890'),
            capacity=50,
            owner=self.user
        )
    
    def test_create_comment(self):
        """تست ایجاد کامنت"""
        comment = Comment.objects.create(
            user=self.user,
            cafe=self.cafe,
            content='کافه خوبی بود',
            rating=4
        )
        
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.cafe, self.cafe)
        self.assertEqual(comment.content, 'کافه خوبی بود')
        self.assertEqual(comment.rating, 4)
        self.assertFalse(comment.is_verified)
        self.assertIsNotNone(comment.created_at)
    
    def test_comment_str_representation(self):
        """تست نمایش رشته کامنت"""
        comment = Comment.objects.create(
            user=self.user,
            cafe=self.cafe,
            content='کافه خوبی بود',
            rating=4
        )
        expected = f"کامنت {self.user.first_name} برای {self.cafe.name}"
        self.assertEqual(str(comment), expected)
    
    def test_comment_rating_validation(self):
        """تست validation امتیاز کامنت"""
        # امتیاز نامعتبر (کمتر از 1)
        with self.assertRaises(ValidationError):
            comment = Comment(
                user=self.user,
                cafe=self.cafe,
                content='کافه بد بود',
                rating=0
            )
            comment.full_clean()
        
        # امتیاز نامعتبر (بیشتر از 5)
        with self.assertRaises(ValidationError):
            comment = Comment(
                user=self.user,
                cafe=self.cafe,
                content='کافه عالی بود',
                rating=6
            )
            comment.full_clean()
    
    def test_comment_auto_rating_update(self):
        """تست به‌روزرسانی خودکار امتیاز کافه پس از کامنت"""
        initial_rating = self.cafe.average_rating
        
        comment = Comment.objects.create(
            user=self.user,
            cafe=self.cafe,
            content='کافه خوبی بود',
            rating=4
        )
        
        # امتیاز کافه باید به‌روزرسانی شده باشد
        self.cafe.refresh_from_db()
        self.assertNotEqual(self.cafe.average_rating, initial_rating)
        self.assertEqual(self.cafe.average_rating, Decimal('4.00'))
        self.assertEqual(self.cafe.total_reviews, 1)

