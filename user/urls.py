from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    # Authentication URLs
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Profile URLs
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/detail/', views.UserProfileDetailView.as_view(), name='profile_detail'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    
    # Dashboard and Location
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('update-location/', views.update_location, name='update_location'),
]
