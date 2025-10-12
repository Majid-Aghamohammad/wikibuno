from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

from .models import User, UserProfile
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserSerializer, 
    UserUpdateSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer
)

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    """
    View برای ثبت‌نام کاربر جدید
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'کاربر با موفقیت ثبت شد',
                'user': UserSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    """
    View برای لاگین کاربر
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        return Response({
            'message': 'ورود موفقیت‌آمیز',
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    """
    View برای خروج کاربر
    """
    try:
        request.user.auth_token.delete()
        logout(request)
        return Response({
            'message': 'خروج موفقیت‌آمیز'
        }, status=status.HTTP_200_OK)
    except:
        return Response({
            'error': 'خطا در خروج'
        }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    View برای مشاهده و ویرایش پروفایل کاربر
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    View برای مشاهده و ویرایش جزئیات پروفایل کاربر
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


class ChangePasswordView(generics.UpdateAPIView):
    """
    View برای تغییر رمز عبور
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = self.get_object()
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({
                'message': 'رمز عبور با موفقیت تغییر کرد'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_dashboard(request):
    """
    View برای داشبورد کاربر
    """
    user = request.user
    profile = user.profile
    
    # آمار کاربر
    stats = {
        'owned_cafes': user.owned_cafes.count(),
        'cafe_likes': user.cafe_likes.count(),
        'cafe_comments': user.cafe_comments.count(),
    }
    
    return Response({
        'user': UserSerializer(user).data,
        'profile': UserProfileSerializer(profile).data,
        'stats': stats
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_location(request):
    """
    View برای به‌روزرسانی موقعیت مکانی کاربر
    """
    latitude = request.data.get('latitude')
    longitude = request.data.get('longitude')
    location = request.data.get('location', '')
    
    if not latitude or not longitude:
        return Response({
            'error': 'عرض و طول جغرافیایی الزامی است'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        profile = request.user.profile
        profile.latitude = float(latitude)
        profile.longitude = float(longitude)
        profile.location = location
        profile.save()
        
        return Response({
            'message': 'موقعیت مکانی به‌روزرسانی شد',
            'location': {
                'latitude': profile.latitude,
                'longitude': profile.longitude,
                'address': profile.location
            }
        }, status=status.HTTP_200_OK)
    except ValueError:
        return Response({
            'error': 'مقادیر جغرافیایی نامعتبر است'
        }, status=status.HTTP_400_BAD_REQUEST)
