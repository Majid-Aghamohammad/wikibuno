from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Cafe, CafeMenu, Like, Comment

User = get_user_model()


class CafeMenuSerializer(serializers.ModelSerializer):
    """
    Serializer برای منوی کافه
    """
    class Meta:
        model = CafeMenu
        fields = '__all__'
        read_only_fields = ('cafe', 'created_at', 'updated_at')


class CafeSerializer(serializers.ModelSerializer):
    """
    Serializer برای کافه
    """
    menu_items = CafeMenuSerializer(many=True, read_only=True)
    owner_name = serializers.CharField(source='owner.first_name', read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Cafe
        fields = '__all__'
        read_only_fields = ('owner', 'average_rating', 'total_reviews', 'created_at', 'updated_at')
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


class CafeCreateSerializer(serializers.ModelSerializer):
    """
    Serializer برای ایجاد کافه جدید
    """
    class Meta:
        model = Cafe
        exclude = ('owner', 'average_rating', 'total_reviews', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class CafeUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer برای ویرایش کافه
    """
    class Meta:
        model = Cafe
        exclude = ('owner', 'average_rating', 'total_reviews', 'created_at', 'updated_at')


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer برای لایک کافه
    """
    user_name = serializers.CharField(source='user.first_name', read_only=True)
    cafe_name = serializers.CharField(source='cafe.name', read_only=True)
    
    class Meta:
        model = Like
        fields = '__all__'
        read_only_fields = ('user', 'created_at')
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate(self, attrs):
        # بررسی تکراری نبودن لایک
        user = self.context['request'].user
        cafe_id = self.context['view'].kwargs.get('cafe_id')
        if Like.objects.filter(user=user, cafe_id=cafe_id).exists():
            raise serializers.ValidationError("شما قبلاً این کافه را لایک کرده‌اید")
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer برای کامنت کافه
    """
    user_name = serializers.CharField(source='user.first_name', read_only=True)
    cafe_name = serializers.CharField(source='cafe.name', read_only=True)
    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CafeListSerializer(serializers.ModelSerializer):
    """
    Serializer برای لیست کافه‌ها (ساده‌تر)
    """
    owner_name = serializers.CharField(source='owner.first_name', read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Cafe
        fields = (
            'id', 'name', 'description', 'cafe_type', 'city', 
            'average_rating', 'total_reviews', 'main_image',
            'owner_name', 'likes_count', 'comments_count', 
            'is_liked', 'created_at'
        )
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


class CafeSearchSerializer(serializers.Serializer):
    """
    Serializer برای جستجوی کافه‌ها
    """
    query = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    cafe_type = serializers.CharField(required=False, allow_blank=True)
    has_wifi = serializers.BooleanField(required=False)
    has_parking = serializers.BooleanField(required=False)
    is_smoking_allowed = serializers.BooleanField(required=False)
    has_outdoor_seating = serializers.BooleanField(required=False)
    min_rating = serializers.DecimalField(max_digits=3, decimal_places=2, required=False)
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False)
    radius = serializers.IntegerField(required=False, default=5)  # کیلومتر


class CafeRecommendationSerializer(serializers.Serializer):
    """
    Serializer برای پیشنهاد کافه‌ها
    """
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=True)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=True)
    radius = serializers.IntegerField(required=False, default=10)  # کیلومتر
    limit = serializers.IntegerField(required=False, default=20)
    cafe_types = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True
    )
