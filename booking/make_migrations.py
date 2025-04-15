"""
This file is a simple helper script to manually run migrations.
To use, run `python booking/migrations/make_migrations.py`
"""

import os
import sys
import django

# Add the project directory to the sys.path
sys.path.append('D:\\projects\\tourism_project')

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tourism_project.settings')

# Initialize Django
django.setup()

# Run the migrations
from django.core.management import call_command
call_command('makemigrations', 'booking')
print("Migrations created successfully. Now run 'python manage.py migrate' to apply them.")
