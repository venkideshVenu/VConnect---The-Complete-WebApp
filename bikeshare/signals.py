# bikeshare/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import BikeShareProfile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_bikeshare_profile(sender, instance, created, **kwargs):
    """Create a BikeShare profile when a new user is created"""
    if created:
        BikeShareProfile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_bikeshare_profile(sender, instance, **kwargs):
    """Save the BikeShare profile whenever the user is saved"""
    if not hasattr(instance, 'bikeshare_profile'):
        BikeShareProfile.objects.create(user=instance)
    else:
        instance.bikeshare_profile.save()

# bikeshare/apps.py
