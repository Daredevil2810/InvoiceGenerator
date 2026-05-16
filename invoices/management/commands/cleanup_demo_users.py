# invoices/management/commands/cleanup_demo_users.py

from django.core.management.base import BaseCommand

from django.contrib.auth.models import User

from django.utils import timezone

from datetime import timedelta

from invoices.models import UserProfile


class Command(BaseCommand):

    help = 'Delete expired demo users'

    def handle(self, *args, **kwargs):

        expiry_time = timezone.now() - timedelta(
            minutes=10
        )

        expired_profiles = UserProfile.objects.filter(

            is_demo_user=True,

            demo_created_at__lt=expiry_time

        )

        count = expired_profiles.count()

        for profile in expired_profiles:

            profile.user.delete()

        self.stdout.write(

            self.style.SUCCESS(

                f'{count} expired demo users deleted.'

            )
        )