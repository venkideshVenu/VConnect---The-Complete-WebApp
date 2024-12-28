# socialhub/management/commands/create_missing_profiles.py

from django.core.management.base import BaseCommand
from core.models import CustomUser
from socialhub.models import Profile

class Command(BaseCommand):
    help = 'Create missing profiles for users'

    def handle(self, *args, **kwargs):
        users = CustomUser.objects.all()
        created_count = 0
        
        for user in users:
            profile, created = Profile.objects.get_or_create(user=user)
            if created:
                created_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} missing profiles'
            )
        )