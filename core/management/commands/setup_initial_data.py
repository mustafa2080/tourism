from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

class Command(BaseCommand):
    help = 'Setup initial data for the application'

    def handle(self, *args, **options):
        with transaction.atomic():
            # Create or update the default site
            site, created = Site.objects.get_or_create(
                pk=1,
                defaults={
                    'domain': 'web-production-cfed.up.railway.app',
                    'name': 'Tourism Project'
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created site: {site.domain}')
                )
            else:
                site.domain = 'web-production-cfed.up.railway.app'
                site.name = 'Tourism Project'
                site.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Updated site: {site.domain}')
                )

            # Create superuser if it doesn't exist
            if not User.objects.filter(is_superuser=True).exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@example.com',
                    password='admin123',
                    first_name='Admin',
                    last_name='User'
                )
                self.stdout.write(
                    self.style.SUCCESS('Created superuser: admin/admin123')
                )
            else:
                self.stdout.write(
                    self.style.WARNING('Superuser already exists')
                )

            self.stdout.write(
                self.style.SUCCESS('Initial data setup completed successfully!')
            )
