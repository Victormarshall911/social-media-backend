from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates a superuser if none exists'

    def handle(self, *args, **options):
        # Check if any superuser exists
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS('✓ Superuser already exists'))
            return

        # Get credentials from environment variables
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'changeme123')

        # Validate credentials
        if not email or not username or not password:
            self.stdout.write(self.style.ERROR('✗ Missing superuser credentials in environment variables'))
            return

        try:
            # Create superuser
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name='Admin',
                last_name='User'
            )

            self.stdout.write(self.style.SUCCESS(f'✓ Superuser "{username}" created successfully'))
            self.stdout.write(self.style.SUCCESS(f'  Email: {email}'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error creating superuser: {str(e)}'))