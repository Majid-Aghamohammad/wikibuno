#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create superuser
try:
    # First create a regular user
    user = User.objects.create_user(
        username='admin',
        phone_number='09123456789',
        first_name='admin',
        last_name='admin',
        email='admin@example.com',
        password='admin123'
    )
    
    # Then make it a superuser
    user.is_staff = True
    user.is_superuser = True
    user.save()
    
    print(f"Superuser created successfully: {user.phone_number}")
except Exception as e:
    print(f"Error creating superuser: {e}")
    # Check if user already exists
    if User.objects.filter(phone_number='09123456789').exists():
        print("Superuser already exists!")
        # Make existing user a superuser
        user = User.objects.get(phone_number='09123456789')
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print("Existing user promoted to superuser!")
    else:
        print("Unknown error occurred.")
