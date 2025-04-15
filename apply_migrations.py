"""
This file is a simple helper script to manually apply migrations.
To use, run `python apply_migrations.py`
"""

import os
import sys
import django

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tourism_project.settings')

# Initialize Django
django.setup()

# Run the migrations
from django.core.management import call_command

try:
    print("Creating migrations for booking app...")
    call_command('makemigrations', 'booking')
    print("Applying migrations...")
    call_command('migrate', 'booking')
    print("Booking app migrations created and applied successfully.")
except Exception as e:
    print(f"Error during migration: {e}")
    print("Try running these commands manually:")
    print("python manage.py makemigrations booking")
    print("python manage.py migrate booking")
