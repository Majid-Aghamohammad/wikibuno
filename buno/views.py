from rest_framework import status, generics, permissions, filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Avg, Count
# GIS imports removed - using manual distance calculation
import math

from .models import Cafe, CafeMenu, Like, Comment
from .serializers import (
    CafeSerializer, 
    CafeCreateSerializer, 
    CafeUpdateSerializer,
    CafeListSerializer,
    CafeMenuSerializer,
    LikeSerializer,
    CommentSerializer,
    CafeSearchSerializer,
    CafeRecommendationSerializer
)


class CafeListView(generics.ListCreateAPIView):
    """
    View برای لیست کافه‌ها و ایجاد کافه جدید
    """
    queryset = Cafe.objects.filter(is_active=True, is_approved=True).order_by('-average_rating', '-created_at')
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['city', 'cafe_type', 'has_wifi', 'has_parking', 'is_smoking_allowed', 'has_outdoor_seating']
    search_fields = ['name', 'description', 'address', 'city']
    ordering_fields = ['average_rating', 'total_reviews', 'created_at', 'name']
    ordering = ['-average_rating', '-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CafeCreateSerializer
        return CafeListSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CafeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View برای جزئیات، ویرایش و حذف کافه
    """
    queryset = Cafe.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        # برای مشاهده: فقط کافه‌های تایید شده
        # برای ویرایش: کافه‌های خود کاربر یا ادمین
        if self.request.method == 'GET':
            return Cafe.objects.filter(is_active=True, is_approved=True)
        return Cafe.objects.all()
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CafeUpdateSerializer
        return CafeSerializer
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated()]
        return [AllowAny()]
    
    def perform_update(self, serializer):
        cafe = serializer.instance
        user = self.request.user
        
        # فقط مالک کافه یا ادمین می‌تواند ویرایش کند
        if cafe.owner != user and not user.is_staff:
            raise PermissionDenied("شما فقط می‌توانید کافه‌های خود را ویرایش کنید")
        
        # اگر کاربر عادی است، پس از ویرایش نیاز به تایید مجدد دارد
        if not user.is_staff:
            serializer.save(is_approved=False, approved_by=None, approval_date=None)
        else:
            serializer.save()
    
    def perform_destroy(self, instance):
        user = self.request.user
        if instance.owner != user and not user.is_staff:
            raise PermissionDenied("شما فقط می‌توانید کافه‌های خود را حذف کنید")
        instance.delete()


class CafeMenuView(generics.ListCreateAPIView):
    """
    View برای منوی کافه
    """
    serializer_class = CafeMenuSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        cafe_id = self.kwargs['cafe_id']
        # فقط منوی کافه‌های تایید شده نمایش داده می‌شود
        cafe = Cafe.objects.get(id=cafe_id)
        if cafe.is_approved:
            return CafeMenu.objects.filter(cafe_id=cafe_id, is_available=True)
        return CafeMenu.objects.none()
    
    def perform_create(self, serializer):
        cafe_id = self.kwargs['cafe_id']
        cafe = Cafe.objects.get(id=cafe_id)
        user = self.request.user
        
        # فقط مالک کافه یا ادمین می‌تواند منو اضافه کند
        if cafe.owner != user and not user.is_staff:
            raise PermissionDenied("شما فقط می‌توانید منوی کافه‌های خود را ویرایش کنید")
        
        serializer.save(cafe=cafe)


class CafeMenuDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View برای جزئیات آیتم منو
    """
    serializer_class = CafeMenuSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        cafe_id = self.kwargs['cafe_id']
        # فقط منوی کافه‌های تایید شده قابل مشاهده است
        cafe = Cafe.objects.get(id=cafe_id)
        if cafe.is_approved:
            return CafeMenu.objects.filter(cafe_id=cafe_id)
        return CafeMenu.objects.none()
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated()]
        return [AllowAny()]
    
    def perform_update(self, serializer):
        cafe = serializer.instance.cafe
        user = self.request.user
        
        # فقط مالک کافه یا ادمین می‌تواند منو ویرایش کند
        if cafe.owner != user and not user.is_staff:
            raise PermissionDenied("شما فقط می‌توانید منوی کافه‌های خود را ویرایش کنید")
        serializer.save()
    
    def perform_destroy(self, instance):
        user = self.request.user
        if instance.cafe.owner != user and not user.is_staff:
            raise permissions.PermissionDenied("شما فقط می‌توانید منوی کافه‌های خود را حذف کنید")
        instance.delete()


class LikeView(generics.ListCreateAPIView):
    """
    View برای لایک کافه‌ها
    """
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        cafe_id = self.kwargs['cafe_id']
        return Like.objects.filter(cafe_id=cafe_id)
    
    def perform_create(self, serializer):
        cafe_id = self.kwargs['cafe_id']
        cafe = Cafe.objects.get(id=cafe_id)
        
        # بررسی اینکه آیا کاربر قبلاً لایک کرده یا نه
        if Like.objects.filter(user=self.request.user, cafe=cafe).exists():
            raise serializers.ValidationError("شما قبلاً این کافه را لایک کرده‌اید")
        
        serializer.save(user=self.request.user, cafe=cafe)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unlike_cafe(request, cafe_id):
    """
    View برای حذف لایک کافه
    """
    try:
        like = Like.objects.get(user=request.user, cafe_id=cafe_id)
        like.delete()
        return Response({
            'message': 'لایک حذف شد'
        }, status=status.HTTP_200_OK)
    except Like.DoesNotExist:
        return Response({
            'error': 'لایک یافت نشد'
        }, status=status.HTTP_404_NOT_FOUND)


class CommentView(generics.ListCreateAPIView):
    """
    View برای کامنت کافه‌ها
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        cafe_id = self.kwargs['cafe_id']
        return Comment.objects.filter(cafe_id=cafe_id, is_verified=True).order_by('-created_at')
    
    def perform_create(self, serializer):
        cafe_id = self.kwargs['cafe_id']
        cafe = Cafe.objects.get(id=cafe_id)
        serializer.save(user=self.request.user, cafe=cafe)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View برای جزئیات کامنت
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        cafe_id = self.kwargs['cafe_id']
        return Comment.objects.filter(cafe_id=cafe_id)
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated()]
        return [AllowAny()]
    
    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise permissions.PermissionDenied("شما فقط می‌توانید کامنت‌های خود را ویرایش کنید")
        serializer.save()
    
    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise permissions.PermissionDenied("شما فقط می‌توانید کامنت‌های خود را حذف کنید")
        instance.delete()


@api_view(['POST'])
@permission_classes([AllowAny])
def search_cafes(request):
    """
    View برای جستجوی پیشرفته کافه‌ها
    """
    serializer = CafeSearchSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    queryset = Cafe.objects.filter(is_active=True, is_approved=True)
    
    # جستجو بر اساس متن
    if data.get('query'):
        query = data['query']
        queryset = queryset.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(address__icontains=query) |
            Q(city__icontains=query)
        )
    
    # فیلتر بر اساس شهر
    if data.get('city'):
        queryset = queryset.filter(city__icontains=data['city'])
    
    # فیلتر بر اساس نوع کافه
    if data.get('cafe_type'):
        queryset = queryset.filter(cafe_type=data['cafe_type'])
    
    # فیلتر بر اساس امکانات
    if data.get('has_wifi') is not None:
        queryset = queryset.filter(has_wifi=data['has_wifi'])
    
    if data.get('has_parking') is not None:
        queryset = queryset.filter(has_parking=data['has_parking'])
    
    if data.get('is_smoking_allowed') is not None:
        queryset = queryset.filter(is_smoking_allowed=data['is_smoking_allowed'])
    
    if data.get('has_outdoor_seating') is not None:
        queryset = queryset.filter(has_outdoor_seating=data['has_outdoor_seating'])
    
    # فیلتر بر اساس حداقل امتیاز
    if data.get('min_rating'):
        queryset = queryset.filter(average_rating__gte=data['min_rating'])
    
    # جستجو بر اساس موقعیت جغرافیایی
    if data.get('latitude') and data.get('longitude'):
        user_lat = float(data['latitude'])
        user_lng = float(data['longitude'])
        radius = data.get('radius', 5)  # کیلومتر
        
        # محاسبه فاصله (فرمول Haversine)
        def calculate_distance(lat1, lng1, lat2, lng2):
            R = 6371  # شعاع زمین به کیلومتر
            dlat = math.radians(lat2 - lat1)
            dlng = math.radians(lng2 - lng1)
            a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng/2) * math.sin(dlng/2)
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            return R * c
        
        # فیلتر کافه‌های نزدیک
        nearby_cafes = []
        for cafe in queryset:
            distance = calculate_distance(user_lat, user_lng, float(cafe.latitude), float(cafe.longitude))
            if distance <= radius:
                nearby_cafes.append(cafe)
        
        queryset = Cafe.objects.filter(id__in=[cafe.id for cafe in nearby_cafes])
    
    # مرتب‌سازی
    queryset = queryset.order_by('-average_rating', '-total_reviews')
    
    # سریالایز کردن نتایج
    serializer = CafeListSerializer(queryset, many=True, context={'request': request})
    
    return Response({
        'results': serializer.data,
        'count': queryset.count()
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def recommend_cafes(request):
    """
    View برای پیشنهاد کافه‌ها بر اساس موقعیت کاربر
    """
    serializer = CafeRecommendationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    user_lat = float(data['latitude'])
    user_lng = float(data['longitude'])
    radius = data.get('radius', 10)  # کیلومتر
    limit = data.get('limit', 20)
    cafe_types = data.get('cafe_types', [])
    
    # شروع با تمام کافه‌های فعال و تایید شده
    queryset = Cafe.objects.filter(is_active=True, is_approved=True)
    
    # فیلتر بر اساس نوع کافه
    if cafe_types:
        queryset = queryset.filter(cafe_type__in=cafe_types)
    
    # محاسبه فاصله و فیلتر کافه‌های نزدیک
    def calculate_distance(lat1, lng1, lat2, lng2):
        R = 6371  # شعاع زمین به کیلومتر
        dlat = math.radians(lat2 - lat1)
        dlng = math.radians(lng2 - lng1)
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng/2) * math.sin(dlng/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c
    
    # فیلتر کافه‌های نزدیک و مرتب‌سازی بر اساس امتیاز و فاصله
    nearby_cafes = []
    for cafe in queryset:
        distance = calculate_distance(user_lat, user_lng, float(cafe.latitude), float(cafe.longitude))
        if distance <= radius:
            nearby_cafes.append({
                'cafe': cafe,
                'distance': distance
            })
    
    # مرتب‌سازی بر اساس امتیاز (اولویت اول) و فاصله (اولویت دوم)
    nearby_cafes.sort(key=lambda x: (-x['cafe'].average_rating, x['distance']))
    
    # محدود کردن تعداد نتایج
    nearby_cafes = nearby_cafes[:limit]
    
    # سریالایز کردن نتایج
    cafes = [item['cafe'] for item in nearby_cafes]
    serializer = CafeListSerializer(cafes, many=True, context={'request': request})
    
    # اضافه کردن فاصله به نتایج
    results = []
    for i, cafe_data in enumerate(serializer.data):
        cafe_data['distance'] = round(nearby_cafes[i]['distance'], 2)
        results.append(cafe_data)
    
    return Response({
        'results': results,
        'count': len(results),
        'user_location': {
            'latitude': user_lat,
            'longitude': user_lng
        },
        'search_radius': radius
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_cafes(request):
    """
    View برای کافه‌های کاربر (شامل کافه‌های در انتظار تایید)
    """
    cafes = Cafe.objects.filter(owner=request.user).order_by('-created_at')
    
    # آمار کافه‌ها
    stats = {
        'total': cafes.count(),
        'approved': cafes.filter(is_approved=True).count(),
        'pending': cafes.filter(is_approved=False).count(),
        'active': cafes.filter(is_active=True).count(),
        'inactive': cafes.filter(is_active=False).count(),
    }
    
    serializer = CafeListSerializer(cafes, many=True, context={'request': request})
    
    return Response({
        'results': serializer.data,
        'count': cafes.count(),
        'stats': stats
    }, status=status.HTTP_200_OK)
