from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User, UserProfile


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer برای ثبت‌نام کاربر جدید
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('phone_number', 'first_name', 'last_name', 'email', 'password', 'password_confirm')
        extra_kwargs = {
            'phone_number': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("رمزهای عبور مطابقت ندارند")
        return attrs
    
    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("این شماره تلفن قبلاً ثبت شده است")
        return value
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        # ایجاد پروفایل کاربر
        UserProfile.objects.create(user=user)
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer برای لاگین کاربر
    """
    phone_number = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')
        
        if phone_number and password:
            user = authenticate(phone_number=phone_number, password=password)
            if not user:
                raise serializers.ValidationError("شماره تلفن یا رمز عبور اشتباه است")
            if not user.is_active:
                raise serializers.ValidationError("حساب کاربری غیرفعال است")
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError("شماره تلفن و رمز عبور الزامی است")


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer برای پروفایل کاربر
    """
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer برای اطلاعات کاربر
    """
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'first_name', 'last_name', 'email', 'is_active', 'date_joined', 'profile')
        read_only_fields = ('id', 'date_joined', 'is_active')


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer برای به‌روزرسانی اطلاعات کاربر
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer برای تغییر رمز عبور
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("رمزهای عبور جدید مطابقت ندارند")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("رمز عبور فعلی اشتباه است")
        return value
