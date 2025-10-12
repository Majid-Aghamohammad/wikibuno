from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Cafe, CafeMenu, Like, Comment


class CafeMenuInline(admin.TabularInline):
    """
    Inline admin برای منوی کافه
    """
    model = CafeMenu
    extra = 0
    fields = ('name', 'category', 'price', 'is_available', 'is_popular')
    readonly_fields = ('created_at', 'updated_at')


class CommentInline(admin.TabularInline):
    """
    Inline admin برای کامنت‌های کافه
    """
    model = Comment
    extra = 0
    fields = ('user', 'rating', 'content', 'is_verified', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Cafe)
class CafeAdmin(admin.ModelAdmin):
    """
    Admin interface برای مدل Cafe
    """
    list_display = (
        'name', 'owner', 'city', 'cafe_type', 'average_rating', 
        'total_reviews', 'is_approved', 'is_active', 'created_at'
    )
    list_filter = (
        'is_approved', 'is_active', 'is_verified', 'cafe_type', 
        'city', 'has_wifi', 'has_parking', 'created_at'
    )
    search_fields = ('name', 'description', 'address', 'city', 'owner__phone_number')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'average_rating', 'total_reviews')
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('name', 'description', 'cafe_type', 'owner')
        }),
        ('اطلاعات تماس', {
            'fields': ('phone_number', 'address', 'city')
        }),
        ('موقعیت جغرافیایی', {
            'fields': ('latitude', 'longitude')
        }),
        ('اطلاعات کافه', {
            'fields': ('capacity', 'has_wifi', 'has_parking', 'is_smoking_allowed', 'has_outdoor_seating')
        }),
        ('امتیاز و رتبه‌بندی', {
            'fields': ('average_rating', 'total_reviews')
        }),
        ('تصاویر', {
            'fields': ('main_image', 'gallery')
        }),
        ('وضعیت', {
            'fields': ('is_verified', 'is_active', 'is_approved', 'approval_date', 'approved_by')
        }),
        ('ساعات کاری', {
            'fields': ('opening_hours',)
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    inlines = [CafeMenuInline, CommentInline]
    
    actions = ['approve_cafes', 'disapprove_cafes', 'activate_cafes', 'deactivate_cafes']
    
    def approve_cafes(self, request, queryset):
        """
        تایید کافه‌های انتخاب شده
        """
        updated = queryset.update(
            is_approved=True,
            approved_by=request.user,
            approval_date=timezone.now()
        )
        self.message_user(request, f'{updated} کافه تایید شد.')
    approve_cafes.short_description = "تایید کافه‌های انتخاب شده"
    
    def disapprove_cafes(self, request, queryset):
        """
        لغو تایید کافه‌های انتخاب شده
        """
        updated = queryset.update(
            is_approved=False,
            approved_by=None,
            approval_date=None
        )
        self.message_user(request, f'{updated} کافه لغو تایید شد.')
    disapprove_cafes.short_description = "لغو تایید کافه‌های انتخاب شده"
    
    def activate_cafes(self, request, queryset):
        """
        فعال کردن کافه‌های انتخاب شده
        """
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} کافه فعال شد.')
    activate_cafes.short_description = "فعال کردن کافه‌های انتخاب شده"
    
    def deactivate_cafes(self, request, queryset):
        """
        غیرفعال کردن کافه‌های انتخاب شده
        """
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} کافه غیرفعال شد.')
    deactivate_cafes.short_description = "غیرفعال کردن کافه‌های انتخاب شده"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('owner', 'approved_by')


@admin.register(CafeMenu)
class CafeMenuAdmin(admin.ModelAdmin):
    """
    Admin interface برای مدل CafeMenu
    """
    list_display = ('name', 'cafe', 'category', 'price', 'is_available', 'is_popular', 'created_at')
    list_filter = ('category', 'is_available', 'is_popular', 'created_at')
    search_fields = ('name', 'description', 'cafe__name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('اطلاعات آیتم', {
            'fields': ('cafe', 'name', 'description', 'category')
        }),
        ('قیمت و وضعیت', {
            'fields': ('price', 'is_available', 'is_popular')
        }),
        ('تصویر', {
            'fields': ('image',)
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('cafe')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """
    Admin interface برای مدل Like
    """
    list_display = ('user', 'cafe', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__phone_number', 'user__first_name', 'cafe__name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'cafe')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin interface برای مدل Comment
    """
    list_display = ('user', 'cafe', 'rating', 'is_verified', 'created_at')
    list_filter = ('rating', 'is_verified', 'created_at')
    search_fields = ('user__phone_number', 'user__first_name', 'cafe__name', 'content')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('اطلاعات کامنت', {
            'fields': ('user', 'cafe', 'content', 'rating')
        }),
        ('وضعیت', {
            'fields': ('is_verified',)
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    actions = ['verify_comments', 'unverify_comments']
    
    def verify_comments(self, request, queryset):
        """
        تایید کامنت‌های انتخاب شده
        """
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} کامنت تایید شد.')
    verify_comments.short_description = "تایید کامنت‌های انتخاب شده"
    
    def unverify_comments(self, request, queryset):
        """
        لغو تایید کامنت‌های انتخاب شده
        """
        updated = queryset.update(is_verified=False)
        self.message_user(request, f'{updated} کامنت لغو تایید شد.')
    unverify_comments.short_description = "لغو تایید کامنت‌های انتخاب شده"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'cafe')
